# Contributing to MalPython

Thank you for your interest in contributing to MalPython. This is an educational cybersecurity research repository documenting Python supply chain attack techniques.

## Contribution Guidelines

### Types of Contributions Welcome

- **Attack Vectors**: New documentation on Python supply chain attack methods
- **Defense Mechanisms**: Mitigation strategies and detection techniques
- **Code Examples**: Well-documented proof-of-concept code for educational purposes
- **Documentation**: Improvements to explanations, references, and clarity
- **References**: Academic papers, talks, and industry publications relevant to Python security

### Before You Contribute

1. **Ensure Educational Purpose**: Your contribution should advance understanding of attack/defense mechanisms
2. **Verify Legal Compliance**: Contributions must not encourage illegal activity
3. **Check Licensing**: You agree to license your contribution under MIT with attribution to this repository
4. **No Active Exploits**: Do not contribute code actively being used in real-world attacks
5. **Documentation Quality**: Include clear explanations of what, why, and how

### Submission Process

1. **Fork the repository** on GitHub
2. **Create a feature branch**: `git checkout -b feature/your-contribution`
3. **Add your changes** following the repository structure
4. **Document thoroughly**:
   - Add or update README files in affected directories
   - Include references to relevant papers/talks
   - Explain the attack vector or mitigation clearly
   - Link to related code examples

5. **Commit with clear messages**:
   ```
   Add [attack/defense/docs]: brief description
   
   Longer explanation of the contribution
   References: links to relevant papers/talks
   ```

6. **Open a pull request** with:
   - Clear title and description
   - Explanation of educational value
   - Any relevant security considerations
   - References to related research

### Code Standards

- **Python Code**: Follow PEP 8 style guidelines
- **Comments**: Explain the WHY, not the what (code should be self-documenting)
- **Security Warnings**: Add clear warnings if code could be misused
- **Testing**: Include steps to safely test the code example
- **Dependencies**: Minimize external dependencies; document all requirements

### Documentation Standards

- **Markdown**: Use clear, well-structured markdown
- **Clarity**: Write for security professionals, not just experts in Python
- **Examples**: Include practical examples of how/why an attack works
- **Defenses**: When documenting attacks, include detection/mitigation strategies
- **References**: Link to research, papers, and talks
- **Disclaimers**: Include educational/legal disclaimers where appropriate

### Structure for New Examples

When adding a new attack vector example:

```
attacks/[category]/[example-name]/
├── README.md           # Detailed explanation
├── requirements.txt    # Python dependencies
├── exploit.py         # Main proof-of-concept
├── setup.py           # If packaged as example
└── notes.md           # Additional technical details
```

Include in your README:
- **Overview**: What is this attack vector?
- **Prerequisites**: What must be true for this to work?
- **Mechanism**: How does the attack work?
- **Impact**: What can an attacker achieve?
- **Detection**: How can defenders detect this?
- **Mitigation**: How can this be prevented?
- **References**: Links to research

### Conduct

- Be respectful of other contributors
- Focus on technical discussion, not personal attacks
- Remember: this is educational research, not a how-to guide for malice
- Assume good intent but discuss impact carefully

### Questions or Issues?

- Open an issue for questions about contribution process
- Use discussions for security-related feedback
- Email maintainer for concerns about content appropriateness

### Legal Notice

By contributing to this repository, you agree that:
1. Your contributions are your original work
2. You grant permission to license them under MIT
3. You understand this is educational research only
4. Your contributions comply with applicable laws
5. You are not contributing code from active exploits or security vulnerabilities
