# Malicious Module

This module is used to demonstrate common tricks by threat actor to masquerade malicious code.

## Malicious PTH File

A `.pth` file is a text file located in a `site-packages` directory (or equivalent), used by `site.py` module to add directories to `sys.path`. It works by evaluating each line of `.pth` assuming that each only used to import a module.

To abuse this, one need to create a one-line payload.

## Usage

Create `.pth` file to any `site-packages`. The filename can be anything as long as the payload inside is defined in one line. This is not necessary need to be one expression.

See [payload.pth](payload.pth) as example.