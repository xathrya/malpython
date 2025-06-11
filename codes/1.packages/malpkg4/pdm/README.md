# Malicious Package

## Malicious Build Hook (PDM)

Build Python package using `PDM` as build backend.

PDM has [build hooks](https://backend.pdm-project.org/api/#pdm.backend.hooks.base.BuildHookInterface) to support custom package generation, in the form of plugins.

Create `pdm_build.py` and put the code there.

## Preparation

To use `PDM`, we need to make sure it was installed already, which then create `pyproject.toml`.

```sh
pip3 install pdm
```

## Usage

Use the following command to build the package

```sh
python3 -m build 
```

This will call three hooks