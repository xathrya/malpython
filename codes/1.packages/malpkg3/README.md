# Malicious Package

This package is used to demonstrate common tricks by threat actor to masquerade malicious code.

## Malicious Setup (Install Hook)

Malicious code is insert into `setup.py` file.

The code will be executed as part of installation process by package manager (ie: pip). Specifically, it create an install hook to override the `cmdclass` which will be executed during installation.

!! Note: This techniques is deprecated and might no longer work in the future due to change in how pip install the package.

The base64-encoded payload is a command that will be executed as subprocess.

## Usage

To test locally, use following command for building and installing.

```sh
python3 setup.py sdist
pip3 install dist/malpkg2-0.1.0.tar.gz

# or
pip3 install .
```

check for the existence of file `result.txt`.