#Nmap is one of the most widely used network scanners. You can execute it directly from Python using the subprocess module.

"""Explanation:
subprocess.run() safely invokes the Nmap command.
Using list format avoids shell injection risks.
Capturing output allows us to parse and automate decisions.
"""

import subprocess

# Define target and ports
target = "google.com"
ports = "22,80,443"

# Run Nmap with common flags:
# -Pn: skip ping discovery
# -sS: TCP SYN scan (stealth)
# -p: specify ports
command = ["nmap", "-Pn", "-sS", "-p", ports, target]

# Run and capture the output
result = subprocess.run(command, capture_output=True, text=True)

# Print the raw Nmap output
print(result.stdout)
