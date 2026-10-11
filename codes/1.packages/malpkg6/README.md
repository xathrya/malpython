# Malicious Package

This package is used to demonstrate common tricks by threat actor to masquerade malicious code.

## Namespace Package Poisoning

Namespace package poisoning exploits Python's namespace package system to inject malicious code into shared namespace packages like `google.*`, `aws.*`, `azure.*`, or `kubernetes.*`. When installed, the malicious package becomes a parent package that intercepts all imports within that namespace.

### Attack Mechanism

1. Attacker registers a malicious package with a namespace package name
2. User installs it alongside legitimate namespace packages (e.g., `google-cloud-storage`)
3. Both packages share the same namespace (e.g., `google`)
4. Malicious package's `__init__.py` executes, allowing code injection
5. Code executes when ANY code imports from that namespace

### Impact

**High**: 
- Affects all downstream packages that import from the namespace
- Code executes for legitimate imports of namespace packages
- Difficult to detect (looks like legitimate package import)

### Affected Namespaces

Popular targets:
- `google.*` — Google Cloud SDK, libraries
- `aws.*` — AWS SDK and tools
- `azure.*` — Azure SDK and tools
- `kubernetes.*` — Kubernetes clients
- `urllib3.*` — HTTP library
- `requests.*` — HTTP library (if split as namespace)

## Technical Details

### Python Namespace Packages

Python supports three types of packages:

1. **Regular Package** — Has `__init__.py`, single owner
2. **Namespace Package** — No `__init__.py`, can span multiple distributions
3. **PEP 420 Implicit Namespace Package** — Modern, automatic without `__init__.py`

Namespace packages allow multiple distributions to contribute to the same package namespace:

```python
# google-cloud-storage package
google/cloud/storage/__init__.py

# google-auth package  
google/auth/__init__.py

# Both share the "google" namespace
```

### Poison Mechanism

When a namespace package has NO `__init__.py` in the parent, Python searches through all packages on `sys.path` that match that namespace. An attacker can inject code by:

1. Creating a package that registers in the namespace
2. Adding code to the `__init__.py` at namespace level
3. Code executes when the namespace is first imported

```python
# Attacker's malicious google-poisoned package
google/__init__.py  # THIS EXECUTES when "google" is imported
google/some_module.py

# Legitimate google-cloud-storage package
google/cloud/__init__.py
google/cloud/storage/__init__.py
```

When any code does `import google.cloud.storage`, Python:
1. Looks for `google` package
2. Finds malicious `google/__init__.py` first (or executes both)
3. Malicious code executes
4. Then imports `google.cloud.storage`

## Attack Variations

### Variation 1: Direct Namespace Hijacking

Create a package that becomes the primary namespace package:

```
malpkg6-google/
├── setup.py
└── google/
    ├── __init__.py  # Contains malicious code
    ├── cloud/
    │   └── __init__.py
    └── some_module.py
```

### Variation 2: Sibling Namespace Package

Install alongside legitimate packages, code executes due to import ordering:

```
google-legit-package/
└── google/
    ├── legit_module.py
    
malpkg6-google-poisoned/
└── google/
    ├── __init__.py  # MALICIOUS CODE HERE
    └── poison_module.py
```

### Variation 3: Transitive Namespace Injection

Legitimate package (e.g., `my-app`) depends on malicious namespace package:

```
my-app/
└── setup.py requires malpkg6-google-poisoned
    
When my-app is installed, malpkg6-google-poisoned is installed as dependency
```

## Variants in this directory

Two buildable variants are shipped side-by-side, mirroring how namespace poisoning has evolved alongside Python packaging:

| Variant | Namespace style | Payload trigger | Build system |
| --- | --- | --- | --- |
| [`legacy/`](legacy) | Squat `google/` as a regular package | `import google` | `setup.py` + `find_packages()`, PEP 517 shim via `pyproject.toml` |
| [`modern/`](modern) | PEP 420 implicit namespace (no `__init__.py` at `google/`) | `import google.cloud.<anything>` — poisons the shared Google Cloud SDK sub-namespace | pure `pyproject.toml`, `setuptools` with `tool.setuptools.packages.find.namespaces = true` |

Both has same principle - "run attacker code when the victim imports a namespace they trust". The machinary differs:

- The historical attack simply **shipped a regular `google/__init__.py`**. pip wrote it into site-packages and a bare `import google` ran the payload. The attack worked only in environments that didn't already contain a legitimate `google-*` distribution (pip refuses the overlapping file otherwise). The legacy variant here reproduces that shape.
- The intermediate `pkg_resources`-era approach (`namespace_packages=['google']` plus `declare_namespace()` in `__init__.py`) is now both deprecated **and** self-defeating as a payload vehicle: setuptools *strips* the init from the built wheel and replaces it with a `.pth` file, so there's nowhere for the payload to live at the namespace root.
- Modern SDKs ship as PEP 420 implicit namespace packages — **no** `__init__.py` at the namespace root at all. Legitimate PEP 420 code therefore has no top-level file for the attacker to put payload in, so the modern poisoning target shifts one level down to the first *shared* sub-namespace (e.g. `google.cloud`, `azure.identity`, `kubernetes.client`).

## Usage

Go to each case (`legacy/` and `modern/`) for further instruction on building and testing.

## Detection & Mitigation

### Detection Strategies

1. **Package Listing Audit**
   - List installed packages: `pip list`
   - Check for unexpected packages in common namespaces (google, aws, azure)
   - Look for packages with suspicious names or authors

2. **Namespace Package Inspection**
   ```bash
   python3 -c "import google; print(google.__file__)"
   # Check if __init__.py is where expected
   ```

3. **Dependency Tree Analysis**
   ```bash
   pip show <package>  # See dependencies
   pipdeptree         # Visualize dependency tree
   ```

4. **Source Code Review**
   - Inspect `__init__.py` files in namespace packages
   - Check for unexpected imports or code
   - Look for network connections or subprocess calls

5. **Behavioral Monitoring**
   - Monitor imports of namespace packages
   - Alert on code execution during import
   - Track sys.modules changes

### Mitigation Strategies

1. **Explicit Package Management**
   - Pin exact versions of all dependencies
   - Use lock files (pip-compile, poetry.lock, pipenv)
   - Review all transitive dependencies

2. **Namespace Package Policy**
   - Restrict which namespace packages are allowed
   - Use private package repositories
   - Only install from trusted sources

3. **Installation Controls**
   - Use `--no-deps` to skip transitive dependencies (requires manual verification)
   - Install in virtual environments per project
   - Use container-based dependency isolation

4. **Verification**
   - Verify package integrity with checksums
   - Check package provenance (PyPI metadata)
   - Review package contents before installation: `pip install --dry-run`

5. **Monitoring**
   - File integrity monitoring on site-packages
   - Track namespace package imports
   - Alert on unexpected namespace packages

## Real-World Context

**Why this works:**
- Many popular libraries use namespace packages (Google Cloud, AWS, Azure, Kubernetes)
- Users often install multiple packages from same namespace without realizing it
- Namespace package initialization code runs silently
- Minimal code review of `__init__.py` files

**Attacker advantages:**
- Can target high-value namespaces (aws, google, azure)
- Code executes for ANY import from namespace
- Difficult to detect without detailed dependency inspection
- Low barrier to entry (just register package with namespace name)

## References

- [PEP 420 - Implicit Namespace Packages](https://peps.python.org/pep-0420/)
- [PEP 382 - Namespace Packages](https://peps.python.org/pep-0382/)
- [Python Namespace Packages Documentation](https://packaging.python.org/guides/packaging-namespace-packages/)
- [setuptools namespace_packages](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#namespace-packages)

