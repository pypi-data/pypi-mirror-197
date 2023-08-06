# Changelog

All major changes are listed here.

## 0.6.1

### New Features

* `windkit.wtg_cp` function returns the power_coefficient for given wind speeds from an wind turbine generator.
* Added lookup table to convert WAsP Map Editor named projections to EPSG codes. This allows for projection to be autodetected from some GWC files.

### Breaking changes

* Removed `coords` from `windkit.read_gwc`. Instead you should use the separate `west_east`, `south_north`, and `height` arguments. Also removed `**kwargs`, as there was only a single option `header`, which is now its own argument.

### Changes

* Updated pyproj dependency to minimum 3.0
* Added `gen_heights` and `gen_roughnesses` arguments to `windkit.empty.empty_gwc` to allow users to specify these coordinate values.
* Removed the `mode` argument from `windkit.wtg_power`, `windkit.wtg_ct`, and `windkit.wtg_cp`, as they now work with any number of modes in the WTG. If you wish to use a single mode from a wind turbine object, you should select using the `isel` or `sel` method.

### Bug Fixes

* Allow projections that don't have an EPSG code to be added using `windkit.spatial.add_crs`.
* Scalar spatial datasets would fail in `windkit.spatial.count_spatial_points`.
* Ensured that `wk.Workspace.get_gwc` could parse GWC objects from WAsP 12.7 and 12.8 workspaces.
* Fixed bug in `windkit.spatial.to_stacked_point`, where the order of the `west_east` and `south_north` coordinates would be flipped from expected. This caused an issue when converting to `point` and then back to `stacked_point`.
* Prevent creation of NaN values for some curves when using `windkit.read_wtg` to read ``.wtg`` files with different modes and different wind speed tables.
* Bug fix in `wind_climate._is_bwc` where an exception was not properly caught.

## 0.6.0

Several new features in this release including support for Wind Turbines, the ability to convert roughness lines to roughness polygons, and the ability to read PWC files. Several important bug fixes also added.

### New Features

#### Support for wind turbines and AEP data

* New metadata attributes for annual energy production and wind farm flow map
* New class `windkit.WindTurbines` to hold collections of turbine locations and WTGs (power/ct curves and other details).
* Added metadata for wind turbine generator `xarray.Dataset`.
* New plotting function `windkit.plot.plot_wind_turbine_locations`.

#### Ability to convert roughness lines to polygons and back

* New module `windkit.map_conversion` That allows the user to both create polygons from
  lines and convert polygons to lines, based on `geopandas.GeoDataFrame`. It contains
  the following:
  - `LineMap` and `PolyMap` classes: These classes enable conversion and nice plotting
    of their types.
  - `lines2poly` and `poly2lines` helper functions that perform the conversion from
    lines to polygons and from polygons to line respectively, using the library
    `geopandas.GeoDataFrame`.
* New module `windkit.plot.landcover_map` to plot the `geopandas.GeoDataFrame` polygons
  or lines as a map.
* New module `windkit.plot.color` to provide color functions for maps with a focus on
  roughness coloring.
* Class`windkit.LandCoverTable` has a new method `add_colors_to_table` to store colors to be used in map plots.

#### New spatial functionality

* New function `windkit.spatial.interpolate_to_grid` to resample data to a target grid.
* New function `windkit.spatial.get_latitude` that returns data-array of latitude values in wgs84.
* New function `windkit.spatial.count_spatial_points` counts how many points are in a windkit dataset or dataarray.

#### Enhancements to `windkit.get_map.get_ee_map`
* Added NASADEM as elevation dataset
* Added worldcover as landcover dataset
* Added option to convert to vector in the cloud.

#### Ability to read PWC files

* `windkit.read_pwcfile` reads WAsP `.pwc` predicted wind climate file in XML format and returns a weibull wind climate `xarray.Dataset`

### Breaking changes

* Requires `geopandas>=0.11`.
* Requires `rioxarray` for reading raster GIS files.

### Deprecations

### Changes

* To support `pyproj` 3.4.0, changed from `pyproj.crs.CRS.is_exact_same` to `pyproj.crs.CRS.equals`, and dropped deprecated `skip_equivalent` kwarg.
* Drop `south_north` and `west_east` coords before reassigning them as required in [future `xarray` version](https://github.com/pydata/xarray/issues/6505).
* Added height dependent wind direction frequencies to GWC I/O routines
  - For the .lib-file reader frequencies are duplicated across all gen_heights
  - For the .lib-file writer a check is made to ensure all frequencies are these same across heights. If they are not, a gen_height is required to be set by the user.

### Improvements
 * Sped up creation of .lib strings for GWC objects. In testing 15 sites, went from 11s to <1.
 * Retain meta data of `wsbin` coordinates now also present after combining `bwc`'s

### Bug Fixes
* `Windkit.wwc_mean_windspeed`  and `windkit.wwc_power_density` previously calculated emergent wind case using all-sector A&k values. Now it is correctly calculated using sectorwise, and an error is thrown if both `emergent` and `bysector` kwargs are `True`.
* Fixed reading `tif` and `grd` files with negative `dx`.
* Catch exception in `wind_climate._is_bwc`.
* Prevent modification of input dataset when calling `weibull_wind_climate.weibull_combined`.
* Return point or stacked-point dataset for when calling `windkit.spatial.create_dataset` with duplicated `west_east` and `south_north` values. Previously a cuboid was returned with duplicated points collapsed.
* Use fixed column parsing in `read_rsf/read_wrg` rather than space splitting, when reading the number of sectors.
* Ensure temporary file created when using `windkit/get_map.py` is always removed.
* Create correct BWC when reading data with with irregular bins (i.e. as exported from windpro).

## 0.5.1

* Changed name of author's attributes from name/email to author/author_email
* Fixed bug for 1d nearest point estimation. The KDtree throws an error if we do not expand the 2d point [x,y] to [[x],[y]]
* Removed unneeded dependencies

##  0.5.0

### New Features
* Added functions `read_wrgfile` and `to_wrgfile` to read and write .wrf resource grid files
* Added functions for simple wind-related calculations:
   - `windkit.wind_speed_and_direction` calculates wind speed and direction from horizontal wind vectors U and V
   - `windkit.wind_vectors` calculates horizontal wind vectors U and V from wind speed and direction
   - `windkit.wind_direction_difference` calculates the smallest (signed) circular difference between wind directions in degrees.
   - `windkit.wind_speed` calculates horizontal wind speed from vectors U and V
   - `windkit.wind_direction` calculates horizontal wind direction from vectors U and V
   - `windkit.wd_to_sector` to calculate the bin-index for wind directions for a given number of bins/sectors
* Support for new Xarray-based Wind Turbine Generator (WTG) object added
*  New wind climate dataset validator function and decorator.
   - The function receives an `xarray.Dataset` and returns `True` or `False`.
   - The decorator wraps a function that receives a wind climate dataset and raises a `WindClimateValidationError` if the dataset is not valid.
   - It checks dimensions, attributes and data variables.
   - The functions available are:
     - `bwc_validate`,`bwc_validate_wrapper` for binned wind climate dataset, imported from `windkit.binned_wind_climate`
     - `wwc_validate`,`wwc_validate_wrapper` for weibull wind climate dataset, imported from `windkit.weibull_wind_climate`
     - `gwc_validate`,`gwc_validate_wrapper` for generalized wind climate dataset, imported from `windkit.generalized_wind_climate`
     - `ts_validate`,`ts_validate_wrapper` for time series wind climate dataset, imported from `windkit.time_series_wind_climate`

* New `WindClimateValidationError`, raised by the newly introduced wind climate dataset validators.
* New method `BBox.to_geoseries()` that converts Bounding box to `geopandas.Geoseries`
* New `empty` module that generates `xarray.Dataset` instances filled with either `NaN` or meaningful values.
   -  Suitable for testing.
   - Current available functions are:
     - `empty.empty_wasp_site_factors()`: Create empty site-factors dataset
     - `empty.empty_bwc()`: Create empty binned wind climate dataset filled with meaningful random numbers, i.e. they are generated
    with a weibull distribution, the sum of `wdfreq` is 1, etc.
     - `empty.empty_wwc()`: Create empty weibull wind climate dataset filled with meaningful random numbers, e.g.the values from `A`
    are generated from a uniform function between `5` and `10` and the values for `k` from a uniform function between `1.5` and `2.5`.
     - `empty.empty_gwc()`: Create empty generalized wind climate dataset with the data variables are filled with meaningful random
    numbers, e.g. the values from `A` are generated from a uniform function between `5` and `10` and the values for `k` from a uniform function between `1.5` and `2.5`.
     - `empty.empty_met_fields()`: Create empty dataset filed with `met_fields`
     - `empty.empty_z0meso()`: Create empty site_factors with only `z0meso` and `slfmeso`
     - `empty.empty_pwc()`: Create empty predicted wind climate with optional variables
* New plotting functions in module `windkit.plot`
   - `windkit.plot.vertical_profile()` plots the vertical profile of the dataArray or dataArrays introduced.
   - `windkit.plot.time_series()` creates a time series plot.
   - `windkit.plot.single_curve()` and `windkit.plot.power_ct_curves()` add plots for electrical power output curve, thrust curve, RPM, Ct, Cp or any other curve the user wants to pass through.

* New function `windkit.time_series.read_ts_windpro_txt`
   -  Reads windpro format txt file into a `xarray.Dataset`
### Removed
* Removed `windkit.binned_wind_climate.dir_to_sec` in favor of `windkit.wd_to_sector`
* Modules `WaspVectorMap` and `WaspRasterMap` were moved to `pywasp` and are no longer available.
 - Removed legacy WTG objet `WindTurbine`

### Changes

* `windkit/windturbine.py`
    - Added function `read_wtg` to create an `xarray.Dataset` representation of a turbine
    - Added `wtg_power` and `wtg_ct` to return power and ct for given wind speed
    - Added `wtg_to_pywake`, which makes a PyWake wind turbine class from the dataset
 - renamed `vectormap` to `vector_map`
 - renamed `rastermap` to `raster_map`
 - renamed `elevationmap` to `elevation_map`
 - renamed `roughnessmap` to `roughness_map`
 - `windkit.read_elevation_map` and `windkit.read_roughness_map` now reads both raster and vector maps.
 - Changed the default behavior of  `windkit.spatial.clip` for rasters/cuboids so small padding is added to the mask, ensuring that raster/cuboid pixels/cells on the edge of the mask are included in the clipping. The previous behavior can be achieved by setting `pad=False`
 - Updated `windkit.spatial.clip` for `point` `xr.dataset` to always include points that are on the edges of the mask (previously only points inside were included)
 - Updated BWC "header" and GWC "desc" to both be named "wasp_header" (only included for objects originating from WAsP files or methods).
 - Updated to always use "crs" as spatial reference argument name
 - Mirrored `spatial.to_raster` as `spatial.to_cuboid`

### Improvements
 - Updated `read_rsffile` and `read_wrgfile` to automatically infer the number of sectors in the data.
 - Updated `windkit.spatial.clip` so it uses a faster clipping method (`_clip_to_bbox_raster`) when the masking is provided as a `BBox` object. This speeds up clipping speed significantly.
 - Allowed `ws_bins` to be python `range` in `windkit.binned_wind_climate._freqs_to_dataset()`
 - Functions `windkit.spatial.to_point` and `windkit.spatial.to_raster_point` now also work on scalar datasets.
 - Fix bug in `metadata.update_var_attrs` to store "Object type" as the string "None" to properly write to netCDF
 - Landcover GMLs use custom reader/write to ensure compatibility with WAsP & Map Editor
 - Plotting documentation improved by rendering jupyter notebooks on it using `nbsphinx` extension for `sphinx`
 - Plotting testing with jupyter notebooks
