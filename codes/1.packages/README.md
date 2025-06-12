# Malicious Packages

Tricks to execute malicious code by masquerading into python packages.

The purpose of this approach is mostly to compromising developer or end-user, by tricking them to install malicious packages directly or indirectly. Later, it can be chained with multiple actions such as delivering malware, or install persistence.

## Samples

Sample as demonstration of how to insert malicious code into packages.

- `Malpkg1 - Malicious Module`: insert code into module that would be imported or used as dependency by other packages/modules.
- `Malpkg2 - Malicious Setup`: insert code into `setup.py` and execute it during installation
- `Malpkg3 - Malicious Setup (Hook)`: insert code into `setup.py`, override the cmdlet, and execute it during installation
- `Malpkg4 - Malicious Backend Hook`: insert code as a build hook.
- `Malpkg5 - Malicious Entry Points`: create entry points as hook of other tools.

## Distribution

There are two different way to distributes package: `source distribution (dsist)` and `binary distribution (bdist)` often in the form of wheels. 

As implied, source distribution contains the source code of the python package, including `.py` files and other resources. It requires a build process on the user's machine, and involve either `setup.py` or `pyproject.toml` to define how the package should be built. Usually the package has name `pgkname-version.tar.gz`.

Binary distribution contains pre-compiled code in the form of `.pyc` files (compiled bytecode) or platform specific binaries for C/C++ extensions. Usually the package has name `pkgname-version-abi-platform.wheel`

Note that Python shift toward a more declarative and standardized build system (see PEP 517/518).

The legacy approach is using `setup.py` for defining package metadata and dependencies. It uses `setuptools` or `distutils` to specify how the package should be built and installed. The typical command to build and install would be:

```sh
python3 setup.py sdist bdist_wheel
pip3 install .
```

The modern approach is using `pyproject.toml` for the configuration. It separates the build system configuration from package metadata and supports multiple build systems such as `setuptools`, `hatchling`, etc. The typical command to build and install would be:

```sh
python3 -m build
python3 -m pip install .
```