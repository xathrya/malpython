# Malicious Packages

**Supply Chain Compromise via Package Distribution**

## Overview

Malicious packages represent a critical supply chain attack vector where threat actors compromise or masquerade legitimate Python packages on PyPI (Python Package Index). These attacks target developers and end-users, either through direct installation or transitive dependencies.

### Attack Goals

- **Initial Foothold** — Inject malicious code into development or production environments
- **Persistence** — Maintain access across system restarts and package updates
- **Credential Theft** — Capture environment variables, API keys, and credentials
- **Lateral Movement** — Compromise downstream dependencies and related projects

### Attack Execution Timeline

```
Package Creation/Compromise
        ↓
Upload to PyPI (or mirror)
        ↓
Developer/Tool installs package
        ↓
Installation-time Code Execution
        ↓
Malicious code gains foothold
```

## Attack Techniques

### Malpkg1: Direct Module Injection

Insert malicious code directly into importable modules. Malicious code can be implemented as python module, loadable shared library, or other mechanism supported by the interpreter.

**Mechanism**: When package is installed and imported, malicious code executes.
**Execution Context**: User's privileges (pip install)
**Detection Difficulty**: Medium (can be hidden in legitimate-looking imports)

**Example Use Case**: Package providing popular utilities (requests, numpy) modified to exfiltrate credentials.

### Malpkg2: Setup.py Installation Hook

Execute arbitrary code during package installation via `setup.py`.

**Mechanism**: Python's setuptools executes setup.py when installing, allowing arbitrary code execution.
**Execution Context**: Full shell execution during pip install
**Detection Difficulty**: Medium (setup.py code is visible in source distributions)

**Advantage**: Executes with `pip install` before package is even loaded.

### Malpkg3: Setup.py Command Override

Hook into setuptools command processing to execute malicious code.

**Mechanism**: Override setuptools Command class to inject code into build pipeline.
**Execution Context**: During setup.py execution
**Detection Difficulty**: Medium-High (requires understanding setuptools internals)

**Advantage**: More sophisticated than direct setup.py execution; blends with legitimate build process.

### Malpkg4: PEP 517/518 Build Backend Hooks

Leverage modern Python build system (PEP 517/518) for code injection.

**Mechanism**: Custom build backend in pyproject.toml executes during build phase.
**Execution Context**: Build system isolation (limited)
**Detection Difficulty**: High (PEP 517 hooks are less commonly audited)

**Advantage**: Uses modern, preferred build system; harder to detect than legacy setup.py.

### Malpkg5: Entry Point Registration

Create CLI commands or plugin entry points that execute malicious code.

**Mechanism**: Register entry_points in setup.py/pyproject.toml for CLI tools or plugins.
**Execution Context**: Command execution context (when tool is invoked)
**Detection Difficulty**: Medium (entry points are listed in metadata)

**Example**: Hijack common CLI tool entry points (e.g., pytest, black, mypy plugins).

### Malpkg6: Namespace Package Poisoning

Inject module into shared Python namespace (`google.*`, `aws.*`, `azure.*`, `kubernetes.*`, …) so attacker code runs on an import the victim already trusts.

**Mechanism**: Ship a package that registers in a well-known namespace. In the legacy shape, drop a regular `google/__init__.py` into site-packages so bare `import google` executes the payload. In the modern shape, use a PEP 420 implicit namespace package (no `__init__.py` at the namespace root) and plant the payload one level down — the first *shared* sub-namespace, e.g. `google.cloud.__init__`.
**Execution Context**: User's privileges, on first import of the namespace or sub-namespace
**Detection Difficulty**: High (looks like an ordinary namespace import; `pkg_resources`-era declarations are stripped on build, so modern poisoning doesn't resemble the old pattern)

**Two variants shipped**: [`legacy/`](malpkg6/legacy) reproduces the historical `google/__init__.py` squat; [`modern/`](malpkg6/modern) poisons `google.cloud` via PEP 420 implicit namespace packages.

### Malpkg7: Payload in Non-Code Asset

Hide the payload in a file that doesn't look like code — a certificate bundle, locale catalog, image, model weight, config blob — and keep only a short, benign-looking loader in Python.

**Mechanism**: Package ships `certs/ca-bundle.pem` with the correct PEM headers and a 64-column base64 body. The body is not DER — it decodes to Python source. The `__init__.py` loader reads the file, strips the PEM frame, base64-decodes the content, and `exec()`s the bytes at import time. `[tool.setuptools.package-data]` is what carries the asset into the wheel; without it the attack fails post-install.
**Execution Context**: User's privileges, every time the package is imported
**Detection Difficulty**: High (payload sits outside the `.py` tree so source-only scanners miss it; the loader itself is ~25 lines of unremarkable stdlib code)

**Advantage**: Payload can be swapped between releases without touching any `.py` file, which is useful for A/B rotation and for evading hash-based alerts aimed at source files.

## Package Distribution Mechanisms

### Source Distribution (sdist)

Contains source code requiring build on user's machine.

**Format**: `packagename-version.tar.gz`

**Build & install (modern, PEP 517)**:
```sh
# builds both sdist and wheel into dist/
python3 -m build --sdist

# install the built sdist (triggers the build on the user's machine)
pip3 install dist/<packagename>-<version>.tar.gz
```

**Build & install (legacy setup.py)**:
```sh
python3 setup.py sdist
pip3 install dist/<packagename>-<version>.tar.gz
```

**Advantages for Attackers**:
- Can hide malicious code in setup.py/build hooks
- All installation scripts execute with user privileges
- Easier to hide in large codebases

### Binary Distribution (Wheels)

Pre-compiled bytecode or binaries; no build required on the victim machine.

**Format**: `packagename-version-abi-platform.whl`

**Build & install**:
```sh
# builds the wheel (and sdist, unless --wheel is passed) into dist/
python3 -m build

# install the built wheel
pip3 install dist/<packagename>-<version>-py3-none-any.whl
```

To install straight from the source tree without an explicit build step (pip invokes the build backend behind the scenes):
```sh
pip3 install .
```

**Advantages for Attackers**:
- `.pyc` files harder to audit (compiled bytecode)
- No visible build script (if malicious code pre-compiled)
- Faster installation = less scrutiny

## Build System Evolution

### Legacy: setup.py

- Uses `setuptools` or `distutils`
- Build configuration in `setup.py` (Python code)
- Easy to hide malicious code
- Command: `python3 setup.py sdist bdist_wheel`

### Modern: pyproject.toml + PEP 517/518

- Declarative configuration (TOML format)
- Supports multiple build backends (setuptools, flit, poetry, hatchling)
- More standardized but still extensible
- Command: `python3 -m build`

**PEP 517**: Specifies build backend interface  
**PEP 518**: Specifies build system requirements in pyproject.toml

## Detection & Mitigation

### Detection Strategies

1. **Dependency Auditing**
   - Use `pip-audit` to scan for known vulnerable packages
   - Review package SBOM (Software Bill of Materials)
   - Check package provenance

2. **Installation Monitoring**
   - Monitor subprocess execution during pip install
   - Track file system changes during installation
   - Log environment variable access

3. **Source Code Review**
   - Inspect setup.py for suspicious code
   - Review build backend implementations
   - Check for obfuscated imports or dynamic code

4. **Supply Chain Verification**
   - Verify package signatures (when available)
   - Check package integrity with checksums
   - Validate author and maintainer identities

### Mitigation Strategies

1. **Install-time Isolation**
   - Install packages in isolated virtual environments
   - Use containerized build environments
   - Run pip install with reduced privileges

2. **Package Vetting**
   - Review package source code before installation
   - Check package maintenance status (recent updates)
   - Verify authentic package authors on PyPI

3. **Policy & Controls**
   - Restrict pip install to approved package sources
   - Use private PyPI mirrors/registries
   - Enforce code review for all dependencies

4. **Monitoring & Detection**
   - Monitor outbound network connections during installation
   - Alert on unusual subprocess spawning
   - Audit credential access and exfiltration attempts
