# Getting Started with MalPython

Welcome to MalPython — a comprehensive resource for understanding Python supply chain attacks and defensive strategies.

## Who Should Use This?

### Security Professionals (Red Team)

You're interested in understanding supply chain attack techniques:

1. Start with [README.md](README.md) for overview
2. Explore attack vectors in order:
   - [Malicious Packages](codes/1.packages/) — Entry point attacks
   - [Malicious Modules](codes/2.modules/) — Runtime persistence
   - [Malicious Interpreter](codes/3.interpreter/) — System-wide compromise
3. Review [payload examples](payloads/) for operational impact
4. Check [SECURITY.md](SECURITY.md) for responsible disclosure

**Estimated Time**: 2-3 hours for complete overview

### Security Professionals (Blue Team)

You want to understand defenses against supply chain attacks:

1. Read [README.md](README.md) overview
2. Focus on **Detection & Mitigation** sections in each attack vector:
   - [Detection strategies for packages](codes/1.packages/README.md#detection--mitigation)
   - [Monitoring for malicious modules](codes/2.modules/README.md#detection--mitigation)
   - [Interpreter compromise detection](codes/3.interpreter/README.md#detection--mitigation)
3. Review [CONTRIBUTING.md](CONTRIBUTING.md) for adding defensive techniques
4. Look at payload examples to understand what to monitor for

**Estimated Time**: 1-2 hours for defensive focus

### Academics & Researchers

You want material for teaching or research:

1. Read full [README.md](README.md) for context
2. Use attack vectors as **case studies** for:
   - Supply chain security lectures
   - Malware analysis courses
   - Software security seminars
3. Reference attack techniques in papers/thesis
4. Review [References section](README.md#references) for related work
5. Contact maintainer for research collaboration

**Estimated Time**: Varies by use case

## Navigation Quick Links

### By Attack Vector

| Technique | Use For | Time |
|-----------|---------|------|
| [Malicious Packages](codes/1.packages/) | Distribution-time attacks, PyPI compromise | 30 min |
| [Malicious Modules](codes/2.modules/) | Persistence, runtime code injection | 30 min |
| [Malicious Interpreter](codes/3.interpreter/) | System-level compromise, advanced attacks | 45 min |
| [Payloads](payloads/) | Real-world attack scenarios | 20 min |

### By Role

| Role | Start Here | Then Go To | Finally |
|------|-----------|-----------|---------|
| Red Teamer | [Packages](codes/1.packages/) | [Modules](codes/2.modules/) | [Interpreter](codes/3.interpreter/) |
| Defender | [Detection Mitigations](codes/1.packages/README.md#detection--mitigation) | [Module Detection](codes/2.modules/README.md#detection--mitigation) | [Interpreter Detection](codes/3.interpreter/README.md#detection--mitigation) |
| Researcher | [Full README](README.md) | [All Techniques](codes/) | [References](README.md#references) |
| CTF Player | [Attack Type] | [Payloads](payloads/) | Challenge-specific |

## Learning Paths

### Understanding Supply Chain Attacks (2-3 hours)

1. **Conceptual Overview** (15 min)
   - Read: [Attack Vectors section](README.md#attack-vectors)

2. **Shallow Dive** (30 min each technique)
   - [Packages overview](codes/1.packages/README.md#overview)
   - [Modules overview](codes/2.modules/README.md#overview)
   - [Interpreter overview](codes/3.interpreter/README.md#overview)

3. **Deep Technical Dive** (30 min each)
   - [Package installation mechanisms](codes/1.packages/README.md#package-distribution-mechanisms)
   - [Module persistence mechanisms](codes/2.modules/README.md#persistence-mechanisms)
   - [Interpreter modification targets](codes/3.interpreter/README.md#modification-targets)

4. **Real-World Impact** (20 min)
   - [Payload examples](payloads/)
   - Understand realistic attack objectives

### Building Defensive Controls (1-2 hours)

1. **Threat Understanding** (30 min)
   - [What attackers do](README.md#attack-vectors)
   - [Attack execution timelines](codes/1.packages/README.md#attack-execution-timeline)

2. **Detection Strategies** (30 min)
   - [Detecting malicious packages](codes/1.packages/README.md#detection-strategies)
   - [Detecting malicious modules](codes/2.modules/README.md#detection-strategies)
   - [Detecting interpreter compromise](codes/3.interpreter/README.md#detection-strategies)

3. **Mitigation Implementation** (30 min)
   - [Preventing package attacks](codes/1.packages/README.md#mitigation-strategies)
   - [Preventing module injection](codes/2.modules/README.md#mitigation-strategies)
   - [Preventing interpreter compromise](codes/3.interpreter/README.md#mitigation-strategies)

## Setting Up Lab Environment

### Safe Testing (Isolated VM)

```bash
# Create isolated environment
docker run -it --rm ubuntu:latest bash

# Inside container:
# 1. Install Python development tools
apt-get update && apt-get install -y python3 python3-dev

# 2. Clone or copy MalPython into container
git clone <malpython-repo>

# 3. Read attack documentation
# 4. Review proof-of-concept code
# 5. DO NOT RUN payloads on network-connected system
```

### Review Without Execution

The safest approach is **code review only**:

1. Read attack vector documentation
2. Review `.py` files to understand techniques
3. Study detection/mitigation strategies
4. Document findings

Execution should only happen in:
- Isolated VMs with no network
- Air-gapped lab networks
- Authorized security assessments
- CTF/competition environments

## Code Examples Structure

Each attack vector directory contains:

```
technique/
├── README.md           # Detailed explanation
├── technique-name.py   # Main payload
├── requirements.txt    # Dependencies (usually none)
└── notes.md           # Technical details
```

**Reading approach**:
1. Start with README.md for conceptual overview
2. Review Python code for implementation details
3. Check notes.md for technical depth
4. Study detection/mitigation sections

## Common Questions

### Q: Can I use this for real attacks?
**A**: No. This is for authorized research, defense, and education only. Unauthorized access is illegal. See [SECURITY.md](SECURITY.md).

### Q: What's the difference between the three attack types?
**A**: 
- **Packages** — Inject at install time, affects whoever installs the package
- **Modules** — Persist at runtime, affects all Python execution on system
- **Interpreter** — Compromise at binary level, affects ALL Python on system

### Q: How do I test this safely?
**A**: Isolated VM with no network, code review only, or authorized lab environment. Never test on system with:
- Network access
- Real credentials
- Production data
- Live internet connection

### Q: Where are the example attacks?
**A**: 
- Code examples: `codes/[1-3].*/*.py`
- Payloads: `payloads/*/`
- Read, don't execute

### Q: Can I contribute?
**A**: Yes! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. We welcome:
- Additional attack techniques
- Defensive mechanisms
- Better documentation
- Research references

### Q: How do I cite this in academic work?
**A**: Include author and license:
```
MalPython: Python Supply Chain Attack Techniques
by Satria Ady Pradana
Licensed under MIT License
https://github.com/xathrya/malpython
```

## Next Steps

1. **Understand Your Use Case**
   - What role are you (red team/blue team/researcher)?
   - What's your learning goal?
   - How much time do you have?

2. **Choose Your Path**
   - Use the learning paths above
   - Start with overview if new to topic
   - Jump to specific technique if experienced

3. **Read Actively**
   - Take notes on key concepts
   - Understand mechanisms, not just payloads
   - Connect defenses to attacks

4. **Apply Knowledge**
   - Improve your own security posture
   - Design better defenses
   - Contribute improvements back

5. **Stay Ethical**
   - Remember: authorized use only
   - Review [SECURITY.md](SECURITY.md)
   - Respect responsible disclosure

## Support & Questions

- **Issues/Questions**: Open an issue on GitHub
- **Improvements**: See [CONTRIBUTING.md](CONTRIBUTING.md)
- **Security Concerns**: See [SECURITY.md](SECURITY.md) for responsible disclosure

---

**Happy learning!** Start with the attack vector that matches your use case and explore from there.
