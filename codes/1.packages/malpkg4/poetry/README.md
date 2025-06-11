# Malicious Package

## Malicious Build Hook (Poetry)

Build Python package using `Poetry` as build backend.

Poetry has undocumented build hooks capability which exists since earlier version. This build is also unique as it is defined in `.md` file.

## Preparation

To use `poetry-core`, we need to make sure it was installed already, which then create `pyproject.toml`.

```sh
pip3 install poetry-core
```

## Usage

To test locally, use following command for building and installing.

```sh
# build
python3 -m build 

# install
pip3 install dist/malpkg4-0.1.0.tar.gz
```