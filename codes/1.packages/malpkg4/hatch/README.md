# Malicious Package

## Malicious Build Hook (Hatch)

Build Python package using `Hatch` as build backend.

Hatch has [build hooks](https://hatch.pypa.io/latest/plugins/build-hook/custom) to support custom package generation, in the form of plugins.

Build hooks are defined for `wheel` and `sdist`. Add the following entries to `pyproject.toml` to add hook to either `wheel`, `sdist`, or both.

```toml
[tool.hatch.build.targets.wheel.hooks.custom]

[tool.hatch.build.targets.sdist.hooks.custom]

[tool.hatch.build.hooks.custom]

```

then create `hatch_build.py` at root of package.

## Preparation

To use `hatch`, we need to make sure it was installed already, which then create `pyproject.toml`.

```sh
pip3 install hatch
```

This project is modified version of `malpkg1` using `hatch`.

```sh
# initializing the existing project
hatch --no-interactive new --init
```

## Usage

Building with hatch can be done directly by calling hatch, or indirectly by calling python build.

```sh
# direct call
hatch build

# indirect call
python3 -m build 
```

Either command will call two hooks: `initialize` and `finalize`. To call the hook at `clean`, we do

```sh
hatch clean
```