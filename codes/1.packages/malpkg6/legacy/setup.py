from setuptools import setup, find_packages

# Legacy "squat the google namespace" attack.
#
# Historically this is what many of the earliest PyPI
# namespace-squatting attacks looked like. The attack fails if the
# victim installs a legitimate `google-*` package first (pip refuses
# the overlapping file), which is why it later evolved into the
# PEP 420 sub-namespace variant in `../modern/`.
setup(
    name="malpkg6-legacy",
    version="0.1.0",
    author="Satria Ady Pradana",
    description="Simple package to demonstrate malicious package by namespace poisoning",
    packages=find_packages(),
    python_requires=">=3.8",
)
