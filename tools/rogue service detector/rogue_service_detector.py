import subprocess
import xml.etree.ElementTree as ET
import json
import os
from datetime import datetime
import logging

BASELINE_FILE = "rogue_service_baseline.json"
LOG_FILE = "rogue_service_alerts.log"

# ----------------------------
# Logging (audit trail)
# ----------------------------
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ----------------------------
# Risky ports dictionary (simple + defensive)
# ----------------------------
RISKY_PORTS = {
    23: "Telnet (unencrypted remote access)",
    21: "FTP (unencrypted file transfer)",
    445: "SMB (lateral movement exposure)",
    3389: "RDP (remote desktop exposure)",
    5900: "VNC (remote control exposure)",
}

# We scan normal range + explicitly scan risky ports too
SCAN_RANGE = "20-1024"
EXTRA_PORTS = ",".join(str(p) for p in RISKY_PORTS.keys())


# ----------------------------
# Run Nmap and return open ports
# ----------------------------
def run_scan(target: str):
    xml_file = f"{target}_rogue_scan.xml"

    # Scan normal range + explicitly scan risky ports
    ports_arg = f"{SCAN_RANGE},{EXTRA_PORTS}"

    command = ["nmap", "-Pn", "-sS", "-p", ports_arg, target, "-oX", xml_file]
    subprocess.run(command)

    open_ports = []
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for host in root.findall("host"):
        for port in host.findall("ports/port"):
            state_el = port.find("state")
            if state_el is None:
                continue

            if state_el.get("state") == "open":
                port_id = port.get("portid")
                if port_id:
                    open_ports.append(int(port_id))

    return sorted(list(set(open_ports)))


# ----------------------------
# Save baseline (new format)
# ----------------------------
def save_baseline(data: dict):
    with open(BASELINE_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ----------------------------
# Load baseline + migrate old format
# ----------------------------
def load_baseline():
    if not os.path.exists(BASELINE_FILE):
        return {"hosts": {}}

    with open(BASELINE_FILE, "r") as f:
        data = json.load(f)

    # New format
    if isinstance(data, dict) and "hosts" in data and isinstance(data["hosts"], dict):
        return data

    # Old single-host format migration
    if isinstance(data, dict) and "target" in data and "open_ports" in data:
        migrated = {
            "hosts": {
                data["target"]: {
                    "open_ports": sorted(list(set(data["open_ports"]))),
                    "last_baseline_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            }
        }
        save_baseline(migrated)
        print("[*] Migrated old baseline to new multi-host format.")
        return migrated

    # Unknown format fallback
    print("[!] Baseline format not recognized. Resetting baseline structure.")
    fresh = {"hosts": {}}
    save_baseline(fresh)
    return fresh


# ----------------------------
# Threat detection: alert if risky ports open
# ----------------------------
def detect_risky_ports(target: str, open_ports):
    risky_found = [p for p in open_ports if p in RISKY_PORTS]

    print("\n=== Rogue Service Detection Report ===")
    print("Open Ports:", open_ports)

    if not risky_found:
        msg = f"[OK] {target}: No risky ports detected."
        print(msg)
        logging.info(msg)
        return

    print("\n[ALERT] Risky ports detected:")
    for p in risky_found:
        msg = f"[ALERT] {target} has port {p} open - {RISKY_PORTS[p]}"
        print(msg)
        logging.warning(msg)


# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":
    target = input("Enter target (domain/IP): ").strip()
    mode = input("Mode (baseline/detect): ").strip().lower()

    current_ports = run_scan(target)
    baseline_data = load_baseline()

    if "hosts" not in baseline_data:
        baseline_data["hosts"] = {}

    # Add host automatically if new
    if target not in baseline_data["hosts"]:
        baseline_data["hosts"][target] = {
            "open_ports": current_ports,
            "last_baseline_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        save_baseline(baseline_data)
        print(f"[+] New host added to baseline: {target}")
        print(f"[+] Saved open ports: {current_ports}")
        raise SystemExit

    if mode == "baseline":
        baseline_data["hosts"][target] = {
            "open_ports": current_ports,
            "last_baseline_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        save_baseline(baseline_data)
        print(f"[+] Baseline updated for {target}")
        print(f"[+] Saved open ports: {current_ports}")

    elif mode == "detect":
        last_update = baseline_data["hosts"][target].get("last_baseline_update", "unknown")
        print(f"[*] Baseline last updated: {last_update}")
        detect_risky_ports(target, current_ports)

    else:
        print("[!] Invalid mode. Use baseline or detect.")
