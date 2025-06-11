# Malicious Module

This module is used to demonstrate common tricks by threat actor to masquerade malicious code.

## Malicious Autoload with PYTHONSTARTUP

`PYTHONSTARTUP` is an environment variable that point to a Python script. This file is executed at startup for `interactive mode`.

Setting the environment variable should be done before execution of Python. In real world scenario, attacker often use method such as modifying user profile or shell's `rc` script to set environment variable. 

## Usage

Set environment variable `PYTHONSTARTUP` to the absolute path of the script.

```sh
export PYTHONSTARTUP="/tmp/startup.py"
python3
```