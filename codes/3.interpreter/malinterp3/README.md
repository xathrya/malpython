# Malicious Interpreter

This module is used to demonstrate common tricks by threat actor to masquerade malicious code.

## Malicious Embedded Script

Embed python script and run it on startup.

This sample will execute simple python code to write a file in current directory.

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

This sample will create a file `malinterp3.txt` which has content "MalPython Interpreter"

## Undo Patch 

If you want to apply patch in other sample using the same source tree, then make sure to undo the patch. To remove or undo the patch do following.

```sh
# undo the patch
patch -R -p1 -d cpython < changes.patch
```