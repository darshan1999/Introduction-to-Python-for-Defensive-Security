"""
Practical defensive security use case:
Host availability and domain intelligence automation.

Functionality:
- Ping-based availability check
- WHOIS metadata collection
- Structured JSON output

Defensive Security Context:
- Domain enrichment
- Threat intelligence gathering
- SOC automation workflows
"""


import subprocess
import json


domain = "scanme.nmap.org"

# Ping check
ping = subprocess.run(["ping", "-n", "3", domain], capture_output=True, text=True)
reachable = "0% packet loss" in ping.stdout

# WHOIS data
whois = subprocess.run(["whois", domain], capture_output=True, text=True)
whois_data = {}
for line in whois.stdout.splitlines():
    for field in ["Registrar:", "Creation Date:", "Expiry Date:"]:
        if line.startswith(field):
            whois_data[field] = line.split(":", 1)[-1].strip()

report = {
    "domain": domain,
    "reachable": reachable,
    "whois": whois_data
}

print(json.dumps(report, indent=2))
