# Malicious Modules

Tricks to execute malicious code by masquerading as or into Python modules.

The purpose of these techniques are mostly to gain persistence or accessing the compromised machine after exploitation.

## Samples

- `Malmod 1 - Autoload (Site Customize)`: create file that will be automatically loaded for each Python invokation.
- `Malmod 2 - Autoload (PYTHONSTARTUP)`: set environment variable to point to the script that will load or execute payload.
- `Malmod 3 - Autoload (Site)`: add code in `site.py` which will load the malicious Python code.
- `Malmod 4 - Autoload (PYTHONPATH)`: set environment variable to point to a directory for shadowing the existing libraries.
- `Malmod 5 - PTH`: add malicious code to file with .pth extension.
- `Malmod 6 - IPython and Jupyter Kernel Hook`: add malicious module to Jupyter/IPython kernel startup hooks directory.