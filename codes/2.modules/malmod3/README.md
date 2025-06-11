# Malicious Module

This module is used to demonstrate common tricks by threat actor to masquerade malicious code.

## Malicious Autoload with Site Overwrite

`site.py` is a standard module in Python that is automatically imported during startup of the Python interpreter (unless `-S` flag is used). It play crucial role in setting up the runtime environment for Python by configuring the import path and preparing the interpreter environment (interactive or not).

By injecting malicious code into `site.py`, attacker can executed code but only within inter

## Preparation

Find the `site.py` file, usually it was in root of the Python path. Use the following code to find out:

```sh
python3 -c "import site; print(site.__file__)"
```

## Usage

Edit the `site.py` found from the preparation section. Insert the malicious code anywhere as long as it is reachable.