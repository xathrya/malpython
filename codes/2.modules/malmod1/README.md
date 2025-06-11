# Malicious Module

This module is used to demonstrate common tricks by threat actor to masquerade malicious code.

## Malicious Autoload with Site Customize

`sitecustomize.py` is a Python script that allows for site-specific customizations. During startup, Python will search for `sitecustomize.py`, the order is from system to user site dirs. If multiple directories in `sys.path` contain a `sitecustomize.py`, only the first one found will be executed and the rest will be ignored. Therefore, it is important to check whether there is existing `sitecustomize.py`.

Other alternative is `usercustomize.py` which has the same effect.

## Preparation

To find the system path and the `site-packages` location, use following command:

```sh
python3 -m site
```

This will give list of Python path. Pick any of the writeable path for the `site-packages`, usually it relative to the home directory.

## Usage

Put the `sitecustomize.py` to the path you choose and execute Python.