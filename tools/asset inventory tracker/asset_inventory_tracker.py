"""sset Inventory Automation Tool will:

✅ Scan multiple authorized assets
✅ Store open ports per host
✅ Maintain structured inventory file
✅ Track first-seen timestamp
✅ Track last-seen timestamp
✅ Detect newly discovered assets
✅ Update existing assets
✅ Work across multiple runs

This becomes your exposure inventory database."""

import subprocess
import xml.etree.ElementTree as ET
import json
import os
from datetime import datetime

INVENTORY_FILE = "asset_inventory.json"

# ----------------------------
# Run Nmap Scan
# ----------------------------
def run_scan(target):
    xml_file = f"{target}_inventory_scan.xml"
    command = ["nmap", "-Pn", "-sS", "-p", "20-1024", target, "-oX", xml_file]
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
# Load Inventory
# ----------------------------
def load_inventory():
    if not os.path.exists(INVENTORY_FILE):
        return {"assets": {}}

    with open(INVENTORY_FILE, "r") as f:
        return json.load(f)


# ----------------------------
# Save Inventory
# ----------------------------
def save_inventory(data):
    with open(INVENTORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ----------------------------
# Update Asset Inventory
# ----------------------------
def update_inventory(target, open_ports):
    inventory = load_inventory()

    if "assets" not in inventory:
        inventory["assets"] = {}

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if target not in inventory["assets"]:
        inventory["assets"][target] = {
            "open_ports": open_ports,
            "first_seen": current_time,
            "last_seen": current_time
        }
        print(f"[+] New asset discovered: {target}")
    else:
        inventory["assets"][target]["open_ports"] = open_ports
        inventory["assets"][target]["last_seen"] = current_time
        print(f"[+] Asset updated: {target}")

    save_inventory(inventory)


# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":
    targets_input = input("Enter targets (comma separated): ").strip()
    targets = [t.strip() for t in targets_input.split(",")]

    for target in targets:
        print(f"\nScanning {target}...")
        ports = run_scan(target)
        update_inventory(target, ports)

    print("\nInventory updated successfully.")
