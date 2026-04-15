# Description:
# This tool scans a host and maintains a structured inventory of its exposed services.
# It tracks asset visibility over time using JSON-based storage.
import socket
import json
import os
from datetime import datetime

FILE = "asset_inventory.json"

def scan_ports(target, ports):
    open_ports = []

    for port in ports:
        sock = socket.socket()
        sock.settimeout(1)

        if sock.connect_ex((target, port)) == 0:
            open_ports.append(port)

        sock.close()

    return open_ports


def load_inventory():
    if not os.path.exists(FILE):
        return {}

    with open(FILE, "r") as f:
        return json.load(f)


def save_inventory(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)


def update_inventory(target, ports):
    data = load_inventory()

    now = datetime.utcnow().isoformat()

    if target not in data:
        data[target] = {
            "open_ports": ports,
            "first_seen": now,
            "last_seen": now
        }
        print(f"[+] New asset added: {target}")
    else:
        data[target]["open_ports"] = ports
        data[target]["last_seen"] = now
        print(f"[+] Asset updated: {target}")

    save_inventory(data)


if __name__ == "__main__":
    target = input("Enter target: ").strip()
    ports = range(20, 1025)

    results = scan_ports(target, ports)
    update_inventory(target, results)