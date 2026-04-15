#Add logging or export to JSON for later analysis.

import json
from datetime import datetime

def save_results(host, open_ports):
    report = {
        "host": host,
        "timestamp": datetime.utcnow().isoformat(),
        "open_ports": open_ports
    }

    with open("scan_results.json", "w") as f:
        json.dump(report, f, indent=2)

# Save the output
save_results("scanme.nmap.org", [22, 80, 443])
