# Malicious Interpreter

Tricks to execute malicious code which inserted into the python binary. This section focus on modification of the Python source code.

The purpose of this approach is mostly to gain persistence or accessing the compromised machine after exploitation.

The sample will use `Python 3.11.9` as base code and each sample contain patch file, which should be applied to the source code.

## Samples

- `Malinterp 1 - Run on Main`: execute code on entrypoint of the interpreter.
- `Malinterp 2 - Run Payload on New Thread`: spawn new thread and execute the payload on that thread.
- `Malinterp 3 - Run Python Code`: embed python code and execute it.

## Python Source Code

This section will modify the python interpreter. Each sample will have diff file which will be used to patch the source code. First, we need to extract the python 3.11.9 source code as base and then apply the patch.

In general, download the source code as following

```sh
wget https://www.python.org/ftp/python/3.11.9/Python-3.11.9.tar.xz
tar -xf Python-3.11.9.tar.xz
mv Python-3.11.9 cpython
```