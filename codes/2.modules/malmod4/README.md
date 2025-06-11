# Malicious Module

This module is used to demonstrate common tricks by threat actor to masquerade malicious code.

## Malicious Autoload with PYTHONPATH

`PYTHONPATH` is an environment variable that augments Python's `sys.path`, list of directories Python searches for modules and packages. Set this variable to point a directory allow attacker to shadowing existing libraries.

In this sample, we put malicious `requests` library and monkeypatch some functions and delegate the rest to the original library.

Note that this technique is tricky due to dependency resolution. Monkeypatching without renaming the target library to something else is prone to error.

## Usage

Set environment variable `PYTHONPATH` to the absolute path of the directory. In this case, use this directory.

```sh
export PYTHONPATH="/path/to/malmod4"
```

Attacker would choose legit-looking paths suck as `$HOME/.local/lib/python3.x/site-packages`. If so, put the example directory `requests`.

To simulate attack, import requests and then try to do some HTTP requests.

```python
import requests
r = requests.post("http://example.com", json={"user":"MYUSERNAME","pass":"MYPASSWORD"})
```