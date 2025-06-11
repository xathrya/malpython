# Malicious Interpreter

This module is used to demonstrate common tricks by threat actor to masquerade malicious code.

## Malicious Entry Point

Add payload on entry point before starting the Python runtime.

This sample will retrieve environment variable when invoked and print it. This can also be extended with other action such as save to file or sent to attacker-controlled HTTP server.

From program entrypoint Python do several actions to prepare the runtime environment before it's ready to run the Python code.

## Preparation

Download the Python source code and name it as `cpython`.

```sh
mkdir /tmp/workdir 
pushd /tmp/workdir

# get the source code
wget https://www.python.org/ftp/python/3.11.9/Python-3.11.9.tar.xz

# extract the python source code 
tar -xf Python-3.11.9.tar.xz
mv Python-3.11.9 cpython

popd
```

## Build

Patch the source code using the `changes.patch` then build the python

```sh
# copy the file.patch to the same folder as the source code.
cp file.patch /tmp/workdir
pushd /tmp/workdir

# apply the patch
patch -p1 -d cpython < changes.patch

# build the executable
cd cpython
./configure
make

popd
```

## Execute

This sample will only print all environment variables when invoking the python interpreter. You can extend this code to send the payload into remote server.

Make sure you are in source tree or python root directory.

```sh
./python
```

## Undo Patch 

If you want to apply patch in other sample using the same source tree, then make sure to undo the patch. To remove or undo the patch do following.

```sh
# undo the patch
patch -R -p1 -d cpython < changes.patch
```