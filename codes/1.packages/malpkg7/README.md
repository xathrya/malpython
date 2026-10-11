# Malicious Package

This package is used to demonstrate common tricks by threat actor to masquerade malicious code.

## Malicious Code in Non-Code Asset

Put payload as a non-code asset - e.g. certificate bundle, locale catalog, image, model weight, config files, etc - and leaving behind short, benign-looking loader in Python.

This sample ship a file [`certs/ca-bundle.pem`](src/malpkg7/certs/ca-bundle.pem) that looks exactly like a PEM-encoded X.509 certificate. The base64 body is not DER, though — it decodes to Python source that [`__init__.py`](src/malpkg7/__init__.py) `exec()`s at import time.

### Attack Goals

- **Scanner evasion** — payload sits outside the Python source tree
- **Reviewer evasion** — a `.pem` with the correct headers and 64-column
  base64 body passes a casual look
- **Low loader footprint** — the `.py` loader only reads a file and
  calls `exec()`; nothing suspicious to grep for individually

### Impact

**High**:
- Executes every time the package is imported
- Looks like a legitimate TLS-related package
- Trivial to swap the payload without touching any `.py` file (useful
  for A/B swapping variants across package versions)

## Technical Details

### Package layout

```
malpkg7/
├── pyproject.toml                 # setuptools build; package-data ships the asset
├── README.md
└── src/
    └── malpkg7/
        ├── __init__.py            # loader: carve base64 body, decode, exec
        └── certs/
            └── ca-bundle.pem      # fake "certificate"; body is base64 Python
```

### Loader Actions

[`__init__.py`](src/malpkg7/__init__.py) reads the `.pem`, pulls out the lines between `-----BEGIN CERTIFICATE-----` and `-----END CERTIFICATE-----`, joins them, base64-decodes the result, and `exec()`s the decoded bytes. That's the whole loader — about 25 lines of unremarkable stdlib code.

### Payload Content

The payload is the Python code [payload.py](payload.py) which is converted into the bundle by [convert.py](convert.py).

The code will prints:

```
[!] malpkg7: malicious code is running from asset ca-bundle.pem
[!]   user=<current user>
```

### Explicit Declaration

setuptools does not include non-`.py` files inside a package by default. Without the `[tool.setuptools.package-data]` entry in `pyproject.toml`, `certs/ca-bundle.pem` would be left out of the wheel and the loader would silently find nothing to decode — the attack would fail post-install even though it works from the source tree. The `package-data` block in [`pyproject.toml`](pyproject.toml) is what makes the attack portable:

```toml
[tool.setuptools.package-data]
malpkg7 = ["certs/*.pem"]
```

## Usage

```bash
# Build
python3 -m build

# Install
pip install dist/malpkg7-0.1.0-py3-none-any.whl

# Trigger (any import of the package fires the payload)
python3 -c "import malpkg7"
```

Expected output on import:

```
[!] malpkg7: malicious code is running from asset ca-bundle.pem
[!]   user=<current user>
```

## Detection & Mitigation

### Detection

1. **Scan non-`.py` files too.** A base64 body in a `.pem` that
   decodes to UTF-8 text, let alone to Python, is a strong signal.
   Legit cert bodies are DER bytes, not text.
2. **Flag `exec()` / `compile()` / `marshal.loads()` on asset
   contents.** A `.py` file that reads any package data file and
   immediately passes it to `exec` is suspicious regardless of what
   the data looks like.
3. **Hash published assets.** Static assets inside a package rarely
   change across versions; a drive-by swap of `ca-bundle.pem`
   between releases is a signal.
4. **Compare with the legitimate upstream.** For well-known
   namespaces (certifi, locale catalogs, model weights), compare
   the asset hashes against the real upstream distribution.

### Mitigation

1. **Pin package hashes.** `pip install --require-hashes` catches
   silent swaps of either the loader or the asset.
2. **Review package contents, not just metadata.** `pip download
   --no-deps` and inspect the wheel; a `.pem` next to a loader that
   `exec`s files is a review failure.
3. **Isolate installs.** Install untrusted packages in a disposable
   environment first and watch the import for unexpected output or
   outbound connections.

## Comparison with other package attacks

| Attack                       | Where the payload lives               | Covered in |
|------------------------------|----------------------------------------|------------|
| Direct module injection      | A `.py` file inside the package        | [malpkg1](../malpkg1) |
| `setup.py` install hook      | `setup.py`                             | [malpkg2](../malpkg2), [malpkg3](../malpkg3) |
| PEP 517 build hooks          | Build backend plugin                   | [malpkg4](../malpkg4), [malpkg8](../malpkg8) |
| Entry points                 | `[project.entry-points.*]`             | [malpkg5](../malpkg5) |
| Namespace packages           | Package layout                         | [malpkg6](../malpkg6) |
| Implicit dependency          | `install_requires` / `dependencies`    | [malpkg7](../malpkg7) |
| **Non-code asset**           | **A file that looks like data**        | **malpkg7** |
