# MalPython: Python Supply Chain Attack Techniques

A comprehensive educational repository documenting supply chain attack vectors targeting the Python ecosystem. This is a catalog of known attack techniques, defensive strategies, and proof-of-concept code for security research and education.

**Author**: Satria Ady Pradana  
**License**: MIT (see [LICENSE](LICENSE))

## ⚠️ Educational & Authorized Use Only

This repository is intended for **authorized security research, defensive security training, and educational purposes only**. All code and techniques are provided for understanding threats to better defend against them. See [SECURITY.md](SECURITY.md) for responsible disclosure guidelines and legal compliance information.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Repository Structure](#repository-structure)
- [Attack Vectors](#attack-vectors)
- [Use Cases](#use-cases)
- [References](#references)
- [Contributing](#contributing)

## Overview

Python's rich ecosystem and Package Index (PyPI) make it an attractive target for supply chain attacks. Threat actors commonly abuse Python distribution mechanisms to:

1. **Gain Initial Foothold** — Deliver malicious code to development environments
2. **Establish Persistence** — Maintain long-term access through multiple mechanisms
3. **Lateral Movement** — Compromise downstream dependencies and projects

This repository documents three primary backdoor insertion techniques:

| Technique | Mechanism | Impact | Scope |
|-----------|-----------|--------|-------|
| **Malicious Packages** | Compromise or masquerade legitimate packages | High (widespread) | Installation phase |
| **Malicious Modules** | Compromise workflow by executing module at specific trigger | High (transitive) | Import/runtime phase |
| **Malicious Interpreter** | Compromise Python interpreter itself | Critical (system-wide) | All Python execution |

## Quick Start

### Exploring Attack Vectors

```bash
# Browse malicious package techniques
ls -la codes/1.packages/

# Review malicious module examples
ls -la codes/2.modules/

# Study interpreter-level attacks
ls -la codes/3.interpreter/

# Review payload examples
ls -la payloads/
```

Each example includes:
- `README.md` — Detailed explanation of the attack vector
- Proof-of-concept Python code
- Build/deployment instructions
- Detection and mitigation guidance

### Requirements

- Python 3.7+ (`malinterp` using 3.11+)
- pip, setuptools, and build tools
- *Intended for isolated lab environments only*

## Repository Structure

```
malpython/
├── README.md                   # This file
├── LICENSE                     # MIT License
├── SECURITY.md                 # Responsible disclosure & legal guidelines
├── CONTRIBUTING.md             # Contribution guidelines
│
├── codes/                      # Attack vector demonstrations
│   ├── 1.packages/             # Supply chain compromise via packages
│   ├── 2.modules/              # Runtime code injection via modules
│   └── 3.interpreter/          # Python interpreter compromise
│
├── payloads/                   # Real-world payload examples
│   └── cython/                 # Compiled extension examples
│
└── slides/                     # Presentation materials
```

## Attack Vectors

### 1. Malicious Packages (`codes/1.packages/`)

Supply chain attacks via compromised or masqueraded packages on PyPI. Focus on executing code before, during, or after package installation.

**Key Techniques:**
- **Direct Injection** — Insert code into legitimate package modules (malpkg1)
- **Setup Hooks** — Execute arbitrary code during installation via `setup.py` (malpkg2-3)
- **Build Backend Hooks** — Leverage PEP 517/518 build system integration (malpkg4)
- **Entry Points** — Register CLI commands or plugin entry points (malpkg5)
- **Namespace Poisoning** — Hijack shared namespace packages like google.* or aws.* (malpkg6)
- **Implicit Dependencies** — Force installation of malicious transitive dependencies (malpkg7)
- **Dynamic Metadata** — Exploit dynamic pyproject.toml configuration for code execution (malpkg8)

**Impact**: When a user installs a package, malicious code executes with the user's privileges. Can affect downstream packages and infrastructure.

**Learn More**: [codes/1.packages/README.md](codes/1.packages/README.md)

### 2. Malicious Modules (`codes/2.modules/`)

Runtime code injection via transitive dependencies and module manipulation. Focus on executing code triggered by specific events or conditions

**Key Techniques:**
- **Dependency Hijacking** — Inject code into commonly-imported modules
- **__init__.py Poisoning** — Modify initialization files
- **Module Shadowing** — Create modules with names similar to popular libraries
- **Namespace Pollution** — Inject into shared package namespaces

**Impact**: Code executes every time the module is imported, affecting all downstream consumers.

**Learn More**: [codes/2.modules/README.md](codes/2.modules/README.md)

### 3. Malicious Interpreter (`codes/3.interpreter/`)

System-level compromise via Python interpreter manipulation. Focus on tampering Python interpreter to execute custom flow.

**Key Techniques:**
- **Custom Build** — Build modified Python interpreter from source
- **Bytecode Injection** — Inject malicious bytecode into standard library
- **Extension Modules** — Create backdoored C extensions

**Impact**: Affects all Python code executed on the system. Extremely difficult to detect.

**Learn More**: [codes/3.interpreter/README.md](codes/3.interpreter/README.md)

### 4. Payload Examples (`payloads/`)

Real-world attack scenarios demonstrating impact and evasion techniques.

**Examples:**
- **Credential Theft** - Extract and exfiltrate credentials from files or environment.
- **Conditional Execution** — Environment detection and sandbox evasion techniques
- **Anti-Detection** — Techniques to bypass code review, testing, and analysis environments
- **Staging** - Download and execute next stage payloads.

**Learn More**: [payloads/README.md](payloads/README.md)

## Use Cases

### For Security Professionals

- **Threat Intelligence** — Understand attack techniques threat actors use
- **Red Team Exercises** — Authorized penetration testing and security assessments
- **Incident Response** — Identify signs of supply chain compromise
- **Vulnerability Research** — Discover new attack vectors and mitigations

### For Defenders

- **Blue Team Training** — Build detection and response capabilities
- **Policy Development** — Create policies to mitigate supply chain risks
- **Supply Chain Audits** — Assess organizational Python dependencies
- **Security Hardening** — Implement controls to detect malicious code

### For Researchers & Educators

- **Academic Research** — Study supply chain security in open source ecosystems
- **Course Material** — Teach Python security and threat modeling
- **CTF Challenges** — Use code as basis for capture-the-flag exercises
- **Security Awareness** — Demonstrate real-world risks of open source adoption

## References

### Presentations

- [PyCon APAC 2024](https://2024-apac.pycon.id/)

## Contributing

We welcome contributions from security researchers, defensive security professionals, and educators. Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on:

- Types of contributions welcome
- Code and documentation standards
- Submission process
- Legal and ethical considerations

## Disclaimer

This research is provided for **educational and authorized security research purposes only**. Users are responsible for ensuring compliance with all applicable laws and regulations in their jurisdiction. Unauthorized access to computer systems is illegal and unethical.

The authors make no warranty about the accuracy, completeness, or suitability of any code or information. Use at your own risk in authorized lab environments only.

## License

Licensed under the MIT License — see [LICENSE](LICENSE) for details.

**Attribution Required**: If you use this work, please provide attribution to Satria Ady Pradana and reference this repository.

---

**Questions or Feedback?** Open an issue or review [SECURITY.md](SECURITY.md) for responsible disclosure guidelines.