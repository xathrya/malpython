# Malicious Modules

**Runtime Code Injection via Python Module Manipulation**

## Overview

Malicious module injection techniques insert code into Python's module loading system, ensuring execution every time affected modules are imported. This approach provides persistence and affects all downstream consumers of infected dependencies.

### Attack Goals

- **Persistence** — Maintain access across system restarts
- **Automatic Execution** — Code runs on every Python invocation or import
- **Transitive Compromise** — Affect all packages that depend on compromised module
- **Stealth** — Hide payload in initialization and startup routines
- **Privilege Escalation** — Execute with elevated privileges if Python runs as admin

### Attack Execution Timeline

```
Initial Compromise (Package/Setup/Interpreter)
        ↓
Inject code into Python module paths
        ↓
Python startup/import of affected module
        ↓
Malicious module initialization executes
        ↓
Persistence maintains across sessions
```

## Persistence Mechanisms

### Malmod1: sitecustomize.py (Auto-load on Startup)

Inject code into `sitecustomize.py` which automatically loads on every Python invocation.

**Mechanism**: 
- Python searches site-packages for `sitecustomize.py`
- If found, automatically imports it before user code executes
- Executes with full Python privileges in the interpreter context

**Location**: `<python-site-packages>/sitecustomize.py`

**Execution Point**: Python startup, before ANY user code

**Detection Difficulty**: High (requires knowledge of Python startup process)

**Advantages**:
- Executes automatically on every Python invocation
- Difficult to disable without modifying Python installation
- Works silently in background

### Malmod2: PYTHONSTARTUP Environment Variable

Set `PYTHONSTARTUP` to point to malicious script executed in interactive mode.

**Mechanism**:
- When Python interactive shell starts (REPL), loads script from PYTHONSTARTUP
- Useful for interactive development sessions
- Less universal than sitecustomize (only affects interactive shells)

**Execution Point**: Interactive Python shell startup

**Detection Difficulty**: Medium (environment variable visible with `env`)

**Example**:
```bash
export PYTHONSTARTUP=/tmp/malicious_startup.py
python3  # This will execute the malicious script
```

**Advantages**:
- Affects developer workflows (common target)
- Maintains persistence across sessions
- Visible only to those checking environment variables

### Malmod3: site.py Module Injection

Inject code directly into Python's `site.py`, which controls site-package initialization.

**Mechanism**:
- `site.py` is imported early in Python startup
- Modifying it allows code injection into initialization process
- Affects all Python invocations on the system

**Location**: `<python-lib>/site.py`

**Execution Point**: Python startup (after basic interpreter initialization)

**Detection Difficulty**: High (site.py modifications easy to hide)

**Advantages**:
- Executes early in startup process
- Difficult to bypass without reinstalling Python
- Standard Python file (modifications may go unnoticed)

### Malmod4: PYTHONPATH Module Shadowing

Set `PYTHONPATH` to include directory with malicious modules that shadow legitimate libraries.

**Mechanism**:
- PYTHONPATH prepended to module search path (sys.path)
- Allows attacker's modules to be found before standard library
- When legitimate import is called, attacker's version loads instead

**Example**:
```bash
export PYTHONPATH="/tmp/malicious_modules:$PYTHONPATH"
python3 -c "import requests"  # Loads attacker's requests instead
```

**Execution Point**: Module import time

**Detection Difficulty**: Medium-High (requires checking sys.path and import behavior)

**Advantages**:
- Intercepts common library imports (requests, boto3, etc.)
- Attacker's code executes in place of legitimate library
- Can proxy to real library while injecting payload

**Risk**: Breaking application functionality if fake module incomplete.

### Malmod5: .pth Files (Path Configuration)

Abuse `.pth` (path configuration) files to inject code into site-packages.

**Mechanism**:
- `.pth` files in site-packages allow adding paths to sys.path
- Lines starting with `import` execute arbitrary code
- Loaded during site module initialization

**Format**:
```
# malicious.pth
import os; os.system('/tmp/payload.sh')
```

**Location**: `<python-site-packages>/malicious.pth`

**Execution Point**: Early Python startup (during site module initialization)

**Detection Difficulty**: High (requires auditing .pth file contents)

**Advantages**:
- Executes arbitrary code during site initialization
- Very early in startup chain
- Can be obfuscated or split across multiple .pth files

### Malmod6: IPython/Jupyter Kernel Hooks

Inject code into IPython and Jupyter startup hooks for interactive notebook environments.

**Mechanism**:
- IPython/Jupyter have configuration directories with startup scripts
- Hooks in `startup/` directory execute on kernel startup
- Affects data scientists, researchers, and notebooks

**Locations**:
- `~/.ipython/profile_default/startup/`
- `~/.jupyter/` configuration directory

**Execution Point**: IPython/Jupyter kernel startup

**Detection Difficulty**: Medium (hooks visible if system audited)

**Advantages**:
- Targets interactive development (high-value targets)
- Maintains persistence across notebook sessions
- Commonly overlooked in security monitoring

## Detection & Mitigation

### Detection Strategies

1. **Startup Hook Auditing**
   - Audit `sitecustomize.py` for unexpected code
   - Review `site.py` modifications
   - Check `.pth` files for suspicious imports
   - Monitor PYTHONSTARTUP environment variable

2. **Module Import Monitoring**
   - Trace module imports to detect shadowing
   - Monitor sys.path for unexpected entries
   - Check import sources and locations

3. **Environment Monitoring**
   - Audit PYTHONPATH environment variable
   - Monitor .ipython and .jupyter configuration directories
   - Track unexpected Python startup behavior

4. **Process Monitoring**
   - Monitor subprocess spawning during Python startup
   - Alert on network connections from Python startup
   - Track file system access during module initialization

### Mitigation Strategies

1. **File System Protection**
   - Use file integrity monitoring (FIM) on Python installation
   - Make site-packages read-only where possible
   - Restrict write access to .pth and startup directories

2. **Environment Isolation**
   - Use virtual environments per project
   - Minimize shared site-packages modifications
   - Isolate IPython/Jupyter configurations

3. **Regular Audits**
   - Periodically audit startup hook files
   - Review Python installations for modifications
   - Verify package origins and checksums

4. **Access Controls**
   - Restrict write access to Python installation directories
   - Use SELinux/AppArmor to prevent module modifications
   - Enforce non-root Python execution
