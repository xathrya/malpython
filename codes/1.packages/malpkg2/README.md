# Malicious Package

This package is used to demonstrate common tricks by threat actor to masquerade malicious code.

## Malicious Setup

Malicious code is inserted inside of the `setup.py` file.

Malicious code is executed as part of installation process by package manager (ie: pip). Therefore, this can only run once, unless the package is reinstalled.

The payload will find `.env` file and send the content to attacker-controlled server.

## Usage

To test locally, first setup a HTTP server that accept `POST` request. Or see the `server.py`.

create a `.env` in any of the following path: 
- ~/.env
- /.env

use following command for building and installing

```sh
python3 setup.py sdist
pip3 install dist/malpkg2-0.1.0.tar.gz
```

during `pip install`, you should see one or more `POST` request to the server.