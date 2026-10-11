# Malicious Package

## Namespace Poisoning (Legacy)

Poison the namespace with our modules.

## Preparation

Our test will test against legitimate `google` namespace, which we get from `google-auth` package as example.

```sh
python3 -m pip install google-auth
```

Then try to test if import works fine

```python
# check the transitive import
import google.auth
```

## Usage

Building and install the package

```sh
python3 -m build
pip install dist/malpkg6_legacy-0.1.0-py3-non-any.whl
```

Test the import, this will execute our malicious code

```python
import google.auth
```

Since we declare `google/` as our namespace, uninstall the package will attempt to uninstall all the content of directory.