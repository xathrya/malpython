# Malicious Package

This package is used to demonstrate common tricks by threat actor to masquerade malicious code.

## Malicious Module

Malicious code is inserted in package as module (file) or inside of existing module.

Malicious code can be executed multiple time when triggered, which can be anything such as:
- package/modules import.
- function execution (hook)
- event or exception handling (ie: HTTP 404 error)

In this example, our payload is python code that will be executed during import.

## Usage

To test locally, use the following command for building and installing.

```sh
# build
python3 setup.py sdist

# install
pip3 install dist/malpkg1-0.1.0.tar.gz
```

and then import the package

```python
import malpkg1
```