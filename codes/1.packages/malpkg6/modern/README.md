# Malicious Package

## Namespace Poisoning (Modern)

Poison the namespace with our modules.

## Usage

Building and install the package

```sh
python3 -m build
pip install dist/malpkg6_legacy-0.1.0-py3-non-any.whl
```

Test the import, this will execute our malicious code

```python
from google.cloud import *
```