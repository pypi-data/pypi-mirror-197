# (c) 2022 DTU Wind Energy
"""Weibull wind climate module

When measuring over a long period the frequency of occurence of wind speed usually follows a
`Weibull distribution <https://en.wikipedia.org/wiki/Weibull_distribution>`_. It is therefore common
practice in the wind energy industry to use the Weibull *A* and *k*
parameters to denote the wind resource at a certain location.

Because there can be large differences in the wind climate when the wind is
coming from different wind directions, the Weibull distributions are usually specified
per sector.

A valid Weibull wind climate therefore has a dimension ``sector`` and the variables
``A``, ``k`` and ``wdfreq``. Also it must have a valid spatial structure. This module contains
functions that operate on and create weibull wind climates.
"""
import io
import logging
import re
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr
from scipy.special import gamma

from ._validate import create_validator
from .metadata import _WEIB_ATTRS, update_history, update_var_attrs
from .sector import create_sector_coords
from .spatial import _raster, add_crs, is_cuboid, to_raster
from .weibull import _solve_k_vec, weibull_moment

WRG_HEADER_PATTERN = re.compile(
    r"\s*(\d+)\s+(\d+)\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s*",
    re.IGNORECASE,
)

DATA_VAR_DICT_WWC = {"A": ["sector"], "k": ["sector"], "wdfreq": ["sector"]}

REQ_DIMS_WWC = ["sector"]

REQ_COORDS_WWC = [
    "south_north",
    "west_east",
    "height",
    "crs",
    "sector",
    "sector_ceil",
    "sector_floor",
]

wwc_validate, wwc_validate_wrapper = create_validator(
    DATA_VAR_DICT_WWC, REQ_DIMS_WWC, REQ_COORDS_WWC
)


def _get_A_k(wwc, bysector):  # pylint:disable=invalid-name
    """Return the appropriate A & k values from the wwc

    Parameters
    ----------
    wwc: xarray.Dataset
        Weibull Wind Climate object
    bysector: bool
        Should results be returned by sector?

    Returns
    -------
    tuple of xr.DataArray
        A & k DataArrays extracted from wwc
    """
    if bysector:
        A = wwc["A"]
        k = wwc["k"]
    elif "A_combined" in wwc.variables:
        A = wwc["A_combined"]
        k = wwc["k_combined"]
    else:
        A, k = weibull_combined(wwc)

    return A, k


def _has_wrg_header(infile, parse_header=False):
    """Check if a resource file has a WRG-style header
    and optionally parse the params.

    Parameters
    ----------
    infile : str, pathlib.Path, io.StringIO
        Input file to check
    parse_header : bool, optional
        If True, will attemp to parse the header params, by default False

    Returns
    -------
    bool:
        Whether the file has a wrg header
    GridParams, optional:
        Grid parameters parsed from the header, if parse_header=True

    """
    if isinstance(infile, io.StringIO):
        fobj = infile
    else:
        fobj = open(infile)

    line = fobj.readline().strip()

    if not isinstance(infile, io.StringIO):
        fobj.close()

    match = WRG_HEADER_PATTERN.match(line)

    return bool(match)


def _infer_resource_file_nsec(infile, skip_first=True):
    """Infer the number of sectors in resource file by reading
    column 70-72 and converting it to an integer.

    Parameters
    ----------
    infile : str, pathlib.Path, io.StringIO
        Resource file to infer sectors from.

    Returns
    -------
    int
        Number of sectors
    """
    if isinstance(infile, io.StringIO):
        fobj = infile
    else:
        fobj = open(infile)

    # Skip the first line
    if skip_first:
        fobj.readline()

    # Read the second line
    line = fobj.readline()

    if not isinstance(infile, io.StringIO):
        fobj.close()

    return int(line[69:72])  # column 70-72 using python indexing


def _read_resource_file(resource_file, crs, nsec=12, to_cuboid=False, **kwargs):
    """Reads .wrg or .rsf file into a weibull wind climate dataset.

    Parameters
    ----------
    resource_file : str, pathlib.Path, io.StringIO
        Path to resource file
    crs : int, dict, str or CRS
        Value to create CRS object or an existing CRS object
    nsec : int
        Number of sectors in file. Defaults to 12.
    to_cuboid: boolean
        If true, the dataset will be converted to the cuboid spatial
        structure (dimensions south_north, west_east, height).

    Returns
    -------
    wwc: xarray.Dataset
        Weibull wind climate dataset.
    """

    has_wrg_header = _has_wrg_header(resource_file)
    nsec = _infer_resource_file_nsec(resource_file, skip_first=has_wrg_header)

    df = pd.read_fwf(
        resource_file,
        widths=tuple([10, 10, 10, 8, 5, 5, 6, 15, 3] + [4, 4, 5] * nsec),
        header=None,
        skiprows=int(has_wrg_header),
    )

    header = [
        "Name",
        "west_east",
        "south_north",
        "elevation",
        "height",
        "A_combined",
        "k_combined",
        "power_density",
        "nsec",
    ]

    for i in range(1, nsec + 1):
        header += f"f_{i} A_{i} k_{i}".split()

    df.columns = header

    can_be_raster = _raster._can_be_raster(df["west_east"], df["south_north"])

    df = df.set_index(["Name"])

    wwc = df.to_xarray()

    wwc = wwc.assign_coords(point=(("Name",), np.arange(len(df.index))))
    wwc = wwc.swap_dims({"Name": "point"})
    wwc = wwc.assign_coords(
        west_east=(("point",), wwc.west_east.values),
        south_north=(("point",), wwc.south_north.values),
        height=(("point",), wwc.height.values),
    )

    knames = [f"k_{sec}" for sec in range(1, nsec + 1)]
    Anames = [f"A_{sec}" for sec in range(1, nsec + 1)]
    fnames = [f"f_{sec}" for sec in range(1, nsec + 1)]

    wwc["k"] = xr.concat([wwc[n] for n in knames], dim="sector")
    wwc["A"] = xr.concat([wwc[n] for n in Anames], dim="sector")
    wwc["wdfreq"] = xr.concat([wwc[n] for n in fnames], dim="sector")

    wwc["elevation"] = wwc["elevation"].astype(np.float64)
    wwc["k"] = wwc["k"] / 100.0
    wwc["A"] = wwc["A"] / 10.0
    wwc["wdfreq"] = wwc["wdfreq"] / wwc["wdfreq"].sum(dim="sector")

    wwc = wwc.drop_vars(
        ["nsec"]
        + [f"k_{sec}" for sec in range(1, nsec + 1)]
        + [f"A_{sec}" for sec in range(1, nsec + 1)]
        + [f"f_{sec}" for sec in range(1, nsec + 1)]
    )

    wwc = add_crs(wwc, crs)
    wdcenters = create_sector_coords(nsec)
    wwc = wwc.assign_coords(**wdcenters.coords)

    if (not can_be_raster) and to_cuboid:
        logging.warning(
            "_read_resource_file: Data cannot be converted to raster, returning point."
        )
    if can_be_raster and to_cuboid:
        wwc = to_raster(wwc)
    wwc = update_var_attrs(wwc, _WEIB_ATTRS)
    return update_history(wwc)


def read_rsffile(rsffile, crs=None, to_cuboid=False, **kwargs):
    """Reads .rsf file into a weibull wind climate dataset.

    Parameters
    ----------
    rsffile : str, pathlib.Path, io.StringIO
        Path to .rsf file
    crs : int, dict, str or CRS
        Value to create CRS object or an existing CRS object
    to_cuboid: boolean
        If true, the dataset will be converted to the cuboid spatial
        structure (dimensions south_north, west_east, height).

    Returns
    -------
    wwc: xarray.Dataset
        Weibull wind climate dataset.
    """
    return _read_resource_file(rsffile, crs=crs, to_cuboid=to_cuboid)


def read_wrgfile(wrgfile, crs=None, to_cuboid=True, **kwargs):
    """Reads .wrg file into a weibull wind climate dataset.

    Parameters
    ----------
    wrgfile : str, pathlib.Path, io.StringIO
        Path to .wrg file
    crs : int, dict, str or CRS
        Value to create CRS object or an existing CRS object
    to_cuboid: boolean
        If true, the dataset will be converted to the cuboid spatial
        structure (dimensions south_north, west_east, height).

    Returns
    -------
    wwc: xarray.Dataset
        Weibull wind climate dataset.
    """
    return _read_resource_file(wrgfile, crs=crs, to_cuboid=to_cuboid)


def read_pwcfile(pwcfile, spatial_dataset):
    """Reads .pwc predicted wind climate file from WAsP in XML format.
       The .pwc file does not include spatial information, so it must
       be passed as a parameter.

    Parameters
    ----------
    pwcfile: str,pathlib.Path, io.StringIO
        Path to .pwc file
    spatial_dataset: xarray.Dataset
        xarray dataset with the spatial info
    """
    ds = pd.read_xml(
        pwcfile, names=["index", "sector", "sector_width", "wdfreq", "A", "k"]
    )
    ds = ds.set_index("sector")[["A", "k", "wdfreq"]].to_xarray()
    ds = ds.assign_coords(create_sector_coords(ds.sector.size).coords)
    ds = ds.expand_dims(spatial_dataset.dims)
    ds = ds.assign_coords(spatial_dataset.coords)
    wwc = update_var_attrs(ds, _WEIB_ATTRS)
    return update_history(wwc)


def _wrg_header(wwc):
    """Write WWC grid dimensions to WRG header with the format:
          nx ny xmin ymin cell_size

    Parameters
    ----------
    wwc : xarray.Dataset
        Weibull wind climate xarray dataset.

    Returns
    -------
    str
        WRG header.

    """
    nx, ny = _raster._shape(wwc)
    xmin = wwc.west_east.values.min()
    ymin = wwc.south_north.values.min()
    size = _raster._spacing(wwc)
    return f"{nx:>8}{ny:>8}{xmin:>18}{ymin:>18}{size:>15}"


@wwc_validate_wrapper
def _to_resource_file(wwc, rsffile, wrg_header=False):
    """Write weibull wind climate dataset to a resource file (.rsf or .wrg).

    Parameters
    ----------
    wwc : xarray.Dataset
        Weibull wind climate xarray dataset.
    rsffile: str
        Path to resource file
    """

    # TODO: 2. make sure sum of written values sum to 100 or 1000
    # order = ['Name', 'west_east', 'south_north', 'elevation',
    #          'height', 'A_combined', 'k_combined', 'power_density', 'nsec']
    wwc_cp = wwc.copy()

    if wrg_header:
        if not is_cuboid(wwc):
            raise ValueError("WWC must be a 'cuboid' to add WRG header!")
        header = _wrg_header(wwc)

    # The code below this line works if these vars are deleted. It was like that
    # originally.
    wwc_cp = wwc_cp.drop_vars(["sector", "sector_ceil", "sector_floor", "crs"])

    wwc_cp["A"] = (wwc_cp["A"] * 10.0).astype(np.int16)
    wwc_cp["k"] = (wwc_cp["k"] * 100.0).astype(np.int16)
    wwc_cp["wdfreq"] = (wwc_cp["wdfreq"] * 1000.0).astype(np.int16)

    df = wwc_cp["elevation"].to_dataframe().reset_index()
    new_columns = ["point", "Name", "west_east", "south_north", "elevation", "height"]
    df = df.reindex(columns=new_columns)

    df = df.merge(wwc_cp["A_combined"].to_dataframe().reset_index())
    df = df.merge(wwc_cp["k_combined"].to_dataframe().reset_index())
    df = df.merge(wwc_cp["power_density"].to_dataframe().reset_index())
    df.loc[:, "nsec"] = wwc_cp.dims["sector"]

    freq_sec = list(wwc_cp["wdfreq"].groupby("sector"))
    A_sec = list(wwc_cp["A"].groupby("sector"))
    k_sec = list(wwc_cp["k"].groupby("sector"))

    for isec in range(wwc_cp.dims["sector"]):
        wdfreq = freq_sec[isec][1].to_dataframe(name=f"wdfreq_{isec+1}").reset_index()
        A = A_sec[isec][1].to_dataframe(name=f"A_{isec+1}").reset_index()
        k = k_sec[isec][1].to_dataframe(name=f"k_{isec+1}").reset_index()
        df = df.merge(wdfreq).merge(A).merge(k)

    df = df.drop(columns=["point"])
    nsec = int(df["nsec"].values[0])
    widths_offset = tuple([9, 9, 9, 7, 4, 4, 5, 14, 2] + [3, 3, 4] * nsec)
    str_list = df.to_string(
        header=False,
        index=False,
        index_names=False,
        col_space=widths_offset,
        justify="left",
    )
    with open(rsffile, "w", newline="\r\n") as text_file:
        if wrg_header:
            text_file.write(header + "\n")
        text_file.write(str_list)


def to_rsffile(wwc, rsffile, wrg_header=False):
    """Write weibull wind climate dataset to .rsf file.

    Parameters
    ----------
    wwc : xarray.Dataset
        Weibull wind climate xarray dataset.
    rsffile: str
        Path to .rsf file
    """
    return _to_resource_file(wwc, rsffile, wrg_header=wrg_header)


def to_wrgfile(wwc, wrgfile):
    """Write weibull wind climate dataset to .wrg file.

    Parameters
    ----------
    wwc : xarray.Dataset
        Weibull wind climate xarray dataset.
    wrgfile: str
        Path to .wrg file
    """
    return _to_resource_file(wwc, wrgfile, wrg_header=True)


def read_grdfile(grdfiles, regex_pattern=None, regex_var_order=None):
    """Reads a .grd file into a weibull wind climate dataset.

    Parameters
    ----------
    grdfiles: str or list
        path of .grd file or list of .grd files.

    regex_pattern: re str
        Filename regex pattern to extract height, sector, and variable name.
        Defaults to None.

    regex_var_order: list or tuple
        Order of 'height', 'sector', and 'var' in regex_pattern. Defaults to None.

    Returns
    -------
    wwc: xarray.Dataset
        Weibull wind climate dataset.
    """

    def _rename_var(var):
        """
        Function to rename WAsP variable names to short hand name
        """
        _rename = {
            "Flow inclination": "flow_inc",
            "Mean speed": "ws_mean",
            "Meso roughness": "meso_rgh",
            "Obstacles speed": "obst_spd",
            "Orographic speed": "orog_spd",
            "Orographic turn": "orog_trn",
            "Power density": "power_density",
            "RIX": "rix",
            "Roughness changes": "rgh_change",
            "Roughness speed": "rgh_spd",
            "Sector frequency": "wdfreq",
            "Turbulence intensity": "tke",
            "Weibull-A": "A",
            "Weibull-k": "k",
            "Elevation": "elevation",
        }

        return _rename[var]

    def _read_grd_data(filename):
        def _parse_line_floats(f):
            return [float(i) for i in f.readline().strip().split()]

        def _parse_line_ints(f):
            return [int(i) for i in f.readline().strip().split()]

        with open(filename, "rb") as f:
            _ = f.readline().strip().decode()  # file_id
            nx, ny = _parse_line_ints(f)
            xl, xu = _parse_line_floats(f)
            yl, yu = _parse_line_floats(f)
            zl, zu = _parse_line_floats(f)
            values = np.genfromtxt(f)

        xarr = np.linspace(xl, xu, nx)
        yarr = np.linspace(yl, yu, ny)

        # note that the indexing of WAsP grd file is 'xy' type, i.e.,
        # values.shape == (xarr.shape[0], yarr.shape[0])
        # we need to transpose values to match the 'ij' indexing
        values = values.T

        return xarr, yarr, values

    def _parse_grdfile(grdfile, regex_pattern=None, regex_var_order=None):
        match = re.findall(regex_pattern, grdfile.name)[0]
        meta = {k: v for k, v in zip(regex_var_order, match)}
        meta["var"] = _rename_var(meta["var"])

        xarr, yarr, values = _read_grd_data(grdfile)

        dims = ["west_east", "south_north", "height"]
        coords = {
            "height": [float(meta["height"])],
            "x": (("west_east",), xarr),
            "y": (("south_north",), yarr),
            "west_east": (("west_east",), xarr),
            "south_north": (("south_north",), yarr),
        }
        values = values[..., np.newaxis]

        if not meta["sector"].lower() == "all":
            dims += ["sector"]
            coords["sector"] = [int(meta["sector"])]
            values = values[..., np.newaxis]
        else:
            if meta["var"] != "elevation":
                meta["var"] = meta["var"] + "_combined"

        da = xr.DataArray(values, dims=dims, coords=coords, name=meta["var"])

        if da.name == "elevation":
            da = da.isel(height=0, drop=True)

        return da

    if not isinstance(grdfiles, list):
        grdfiles = [grdfiles]

    grdfiles = list(Path(f) for f in grdfiles)

    if regex_pattern is None:
        regex_pattern = r"Sector (\w+|\d+) \s+ Height (\d+)m \s+ ([a-zA-Z0-9- ]+)"

    if regex_var_order is None:
        regex_var_order = ("sector", "height", "var")

    wwc = xr.merge(
        [
            _parse_grdfile(
                grdfile, regex_pattern=regex_pattern, regex_var_order=regex_var_order
            )
            for grdfile in grdfiles
        ]
    )

    ds = update_var_attrs(wwc, _WEIB_ATTRS)
    return update_history(ds)


def weibull_combined(wwc):
    """Return the all sector A & k.

    This is know as the combined weibull A and k in the
    WAsP GUI. For more information, see here:
    https://www.wasp.dk/support/faq#general__emergent-and-combined-weibull-all-sector-distributions
    Using the combined weibull A and k are calculated
    using first and third moment conservation rules.

    Parameters
    ----------
    wwc: xarray.Dataset
        Weibull Wind Climate dataset.

    Returns
    -------
    tuple of xr.DataArray
        All sector A & k DataArrays
    """
    sum1 = (wwc["wdfreq"] * weibull_moment(wwc["A"], wwc["k"], 1)).sum(dim="sector")
    sum3 = (wwc["wdfreq"] * weibull_moment(wwc["A"], wwc["k"], 3)).sum(dim="sector")
    sum1 = sum1 / wwc["wdfreq"].sum("sector")
    sum3 = sum3 / wwc["wdfreq"].sum("sector")

    aa = np.log(sum3) / 3.0 - np.log(sum1)
    k_combined = _solve_k_vec(aa)
    A_combined = sum1 / gamma(1.0 + 1.0 / k_combined)

    return A_combined, k_combined


def wwc_mean_windspeed(wwc, bysector=False, emergent=True):
    """Calculate the mean wind speed from a weibull wind climate dataset.

    Parameters
    ----------
    wwc: xarray.Dataset
        Weibull Wind Climate dataset.
    bysector: bool
        Return results by sector or as an all-sector value. Defaults to False.
    emergent: bool
        Calculate the all-sector mean using the emergent (True) or the combined Weibull
        distribution (False). Defaults to True.

    Returns
    -------
    xarray.DataArray
        DataArray with the mean wind speed.
    """
    if bysector and emergent:
        raise ValueError(
            "Emergent wind speed cannot be calculated for sectorwise wind speed."
        )

    if emergent:
        A, k = _get_A_k(wwc, bysector=True)  # emergent always use all sectors
        return (wwc["wdfreq"] * weibull_moment(A, k, 1)).sum(dim="sector")
    else:
        A, k = _get_A_k(wwc, bysector=bysector)
        return weibull_moment(A, k, 1)


def wwc_power_density(wwc, air_density, bysector=False, emergent=True):
    """Calculate the power density

    Parameters
    ----------
    wwc: xarray.Dataset
        Weibull wind climate dataset.
    air_density :  float
        Air density.
    bysector: bool
        Return sectorwise mean wind speed if True. defaults to False.
    emergent: bool
        Calculate the all-sector mean using the emergent (True) or the combined Weibull
        distribution (False). Defaults to True.

    Returns
    pd : xarray.DataArray
        Data array with power density.
    """
    if bysector and emergent:
        raise ValueError(
            "Emergent power density cannot be calculated for sectorwise wind speed."
        )
    if emergent:
        A, k = _get_A_k(wwc, bysector=True)
        pd = (air_density * wwc["wdfreq"] * weibull_moment(A, k, 3.0)).sum(dim="sector")
    else:
        A, k = _get_A_k(wwc, bysector=bysector)
        pd = air_density * weibull_moment(A, k, 3)
    return 0.5 * pd
