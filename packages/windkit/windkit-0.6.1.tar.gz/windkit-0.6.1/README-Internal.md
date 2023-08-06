# WindKit

This project provides common xarray data structures for several wind energy related data formats, as well as plotting and spatial manipulation routines.

## Downstream projects:

- [daTap](https://gitlab-internal.windenergy.dtu.dk/ram/software/tech-team/web-apps/daTap)
- [PyWAsP](https://gitlab-internal.windenergy.dtu.dk/ram/software/pywasp/pywasp)
- [PyWAsP Swarm](https://gitlab-internal.windenergy.dtu.dk/ram/software/pywasp/pywasp-swarm)
- [WindSider Validation](https://gitlab.windenergy.dtu.dk/windsider)

## Developer documentation

[Developer documentation](https://ram.pages-internal.windenergy.dtu.dk/software/pywasp/pywasp-developer-docs/) is maintained in the [Pywasp Developer Docs repository](https://gitlab-internal.windenergy.dtu.dk/ram/software/pywasp/pywasp-developer-docs) using mkdocs.

### Use of lock files

`conda-lock --mamba -f dev_env.yaml -p linux-64 -p osx-64 -p win-64`
`mamba create -n pywasp_env --file conda-lock_linux-64.lock`

## Build and deploy new version

Make sure `CHANGELOG.md` is updated with all changes since last release, and add the correct version.

```sh
export SETUPTOOLS_SCM_PRETEND_VERSION=<version>
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=<global-token> # global token can be found in bitwarden under pypi, username wasp

# Create build environment
mamba create -n build boa build python=3.9 twine setuptools_scm
conda activate build

# install the package such that the above version code (in SETUPTOOLS_SCM_PRETEND_VERSION) will be written to the dist package that is uplaoded to pypi
pip install --no-deps -e .

# Build & deploy Pypi
rm -r dist
python -m build
python3 -m twine upload dist/*

# Build & deploy conda
# This cannot be done from a submodule folder, windkit must be cloned in a different folder.
rm -r conda_build
export VERSION=<version>
time conda mambabuild -c https://conda.windenergy.dtu.dk/channel/open --output-folder conda_build  ./recipe

scp conda_build/*/*.tar.bz2 VIND-pWEBext01:~/.
ssh VIND-pWEBext01
  sudo mv *.tar.bz2 /mnt/data/external/rw/conda-channel/basic_auth_node_server/conda/open/noarch/.
  sudo chown 1000:1000 /mnt/data/external/rw/conda-channel/basic_auth_node_server/conda/open/noarch/*.tar.bz2
  # This may be running on any of the VIND-pWEBext machines. For now ping neda@dtu.dk to carry out these steps.
  docker exec -it production_conda-channel_ci_deploy_storage /bin/bash
    su conda_deploy
    conda index ~/repos/open/
  # To check whether it worked correctly, go to  https://conda.windenergy.dtu.dk/channel/open/noarch/
```

### Build and deploy docs

Make sure you have an environment with all sphinx related dependencies.


```sh
cd docs
make clean
make html
# Copy to the machine
rsync -avP --delete build/html VIND-pWEBext01:/web/static-documentation/setup_files/windkit_docs/windkit/

ssh VIND-pWEBext01
  cd /web/static-documentation/setup_files/windkit_docs/
  #login with your dtu username and password
  docker login registry.windenergy.dtu.dk
  docker build -t registry.windenergy.dtu.dk/ram-tech-team/dockerhub-private/docs_windkit:0.5.1 .
  docker push registry.windenergy.dtu.dk/ram-tech-team/dockerhub-private/docs_windkit:0.5.1

  #update docker compose yaml
  cd /web/static-documentation/
  # edit docker-compose.yml to update docs_windkit image tag.
  # run docker stack deploy
  docker stack deploy -c docker-compose.yml static_project_documentation --with-registry-auth

```
