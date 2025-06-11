# Malicious Module

This module is used to demonstrate common tricks by threat actor to masquerade malicious code.

## Malicious Jupyter and IPython Startup

IPython (and Jupyter) has startup hooks at `~/.ipython/profile_default/startup`, where `*.py` module there will be loaded. Therefore, this technique is applicable for IPython, and Jupyter as it use IPython kernel, and will not working when executing Python script in general.

## Usage

Add the [payload.py](payload.py) to `~/.ipython/profile_default/startup/`.