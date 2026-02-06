"""
Demonstrates parsing command-line output using Python.

Key concepts:
- Processing stdout
- Using regex to extract structured data
- Normalizing CLI output for automation

Defensive Security Context:
- Converting raw command output into actionable intelligence
- Commonly used in WHOIS, netstat, and log parsing
"""


import subprocess
import re

domain = "google.com"
result = subprocess.run(["whois", domain], capture_output=True, text=True)

patterns = {
    "Registrar": r"Registrar:\s*(.+)",
    "Created": r"(Creation Date|Created On):\s*(.+)",
    "Expires": r"(Expiry Date|Expiration Date):\s*(.+)"
}

for key, regex in patterns.items():
    match = re.search(regex, result.stdout, re.IGNORECASE)
    if match:
        print(f"{key}: {match.group(len(match.groups()))}")

