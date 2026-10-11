"""
Demonstrating namespace poisoning by injecting a module to the squatted namespace.

Exposed as `google.cloud.poisoned` for callers that explicitly import it;

Not auto-run on `import google.cloud`, it is handled by `__init__.py` file.
"""

import os

def malicious():
    print("[*] Malicious google.poisoned.malicious() executed")


__all__ = ["malicious"]