"""
Domain Availability and WHOIS Checker

Features:
- User input validation
- Cross-platform ping execution
- WHOIS lookup and parsing
- JSON report generation
- Timeout and error handling

Defensive Security Context:
- Domain enrichment automation
- IOC investigation support
- Foundation for threat intelligence pipelines
"""


import subprocess
import platform
import re
import json
#-----------------------------
# 1. Get user input
# -----------------------------
domain= input("Enter domain name: ").strip()

# -----------------------------
# 2. Validate domain format
# -----------------------------
domain_pattern = r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

if not re.match(domain_pattern, domain):
    print("Invalid domain format")
    exit()


# -----------------------------
# 3. Select OS-specific ping command
# -----------------------------

if platform.system() == "Windows":
    ping_cmd = ["ping", "-n","3",domain]
else:
    ping_cmd = ["ping", "-c","3",domain]

# -----------------------------
# 4. Run ping with error handling
# -----------------------------
try:
    ping_result = subprocess.run(
        ping_cmd,
        capture_output=True,
        text=True,
        timeout=5
    )
    reachable = ping_result.returncode == 0
except subprocess.TimeoutExpired:
    reachable = False

# -----------------------------
# 5. Run WHOIS lookup (OS-aware)
# -----------------------------
whois_data = {}

try:
    if platform.system() == "Windows":
        whois_cmd = ["whois", "-accepteula", domain]
    else:
        whois_cmd = ["whois", domain]

    whois_result = subprocess.run(
        whois_cmd,
        capture_output=True,
        text=True,
        timeout=10,
        encoding="utf-8",   # important
        errors="ignore"
    )

    for line in whois_result.stdout.splitlines():
        line = line.strip()
        if line.lower().startswith("registrar:"):
            whois_data["Registrar"] = line.split(":", 1)[1].strip()
        elif "creation date" in line.lower():
            whois_data["Creation Date"] = line.split(":", 1)[1].strip()
        elif "expiry date" in line.lower() or "expiration date" in line.lower():
            whois_data["Expiry Date"] = line.split(":", 1)[1].strip()

except subprocess.TimeoutExpired:
    whois_data["error"] = "WHOIS lookup timed out"

# -----------------------------
# 6. Build final report
# -----------------------------
report = {
    "domain": domain,
    "reachable": reachable,
    "whois": whois_data
}

# -----------------------------
# 7. Output JSON
# -----------------------------
json_output = json.dumps(report, indent=2)
print(json_output)

# -----------------------------
# 8. Bonus: Log to file
# -----------------------------
with open("domain_report.json", "w") as f:
    f.write(json_output)
