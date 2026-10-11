import os

print( "[!] malpkg7: Malicious code is running from asset ca-bundle.pem")
print(f"[!]     user={os.getenv('USER', 'unknown')}")