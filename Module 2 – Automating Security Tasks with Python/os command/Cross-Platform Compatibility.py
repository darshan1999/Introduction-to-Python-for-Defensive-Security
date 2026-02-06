"""
Demonstrates cross-platform command execution.

Key concepts:
- Detecting operating system
- Adapting commands for Windows and Linux/macOS

Defensive Security Context:
- Enables portable security tools
- Essential for enterprise and hybrid environments
"""



import platform
import subprocess

if platform.system() == "Windows":
    cmd = ["ipconfig"]
else:
    cmd = ["ifconfig"]

subprocess.run(cmd)
