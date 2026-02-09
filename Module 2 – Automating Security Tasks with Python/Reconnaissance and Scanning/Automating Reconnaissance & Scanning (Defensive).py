"""
Exercise: Automating Reconnaissance and Scanning with Python

This script:
- Accepts a target (IP or domain)
- Runs an Nmap TCP SYN scan on ports 20-1024 and saves XML output
- Parses Nmap XML output to extract port/service info
- Runs a socket-based validation scan on the same ports
- Logs results to a local file with timestamps
- (Optional logic) prints an alert if port 3389 or 23 is open
"""

import subprocess
import socket
import xml.etree.ElementTree as ET
import logging
from datetime import datetime


# -----------------------------
# Logging setup (timestamps)
# -----------------------------
logging.basicConfig(
    filename="recon_scan.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# -----------------------------
# 1) Run Nmap and save XML
# -----------------------------
def run_nmap_scan(target: str) -> str:
    xml_file = "nmap_output.xml"
    command = [
        "nmap",
        "-Pn",
        "-sS",
        "-p", "20-1024",
        target,
        "-oX", xml_file
    ]

    try:
        # Note: timeout here applies to the whole Nmap execution
        subprocess.run(command, capture_output=True, text=True, timeout=120)
        return xml_file
    except subprocess.TimeoutExpired:
        logging.error("Nmap scan timed out.")
        raise
    except FileNotFoundError:
        # This happens if nmap is not installed or not in PATH
        logging.error("Nmap not found. Make sure Nmap is installed and in PATH.")
        raise


# -----------------------------
# 2) Parse Nmap XML results
# -----------------------------
def parse_nmap_xml(xml_file: str):
    results = []

    tree = ET.parse(xml_file)
    root = tree.getroot()

    for host in root.findall("host"):
        address = host.find("address")
        if address is None:
            continue

        ip = address.get("addr", "unknown")

        for port in host.findall("ports/port"):
            port_id = port.get("portid")
            protocol = port.get("protocol")

            state_el = port.find("state")
            state = state_el.get("state") if state_el is not None else "unknown"

            service_el = port.find("service")
            service = service_el.get("name", "unknown") if service_el is not None else "unknown"

            results.append({
                "ip": ip,
                "port": int(port_id) if port_id else None,
                "protocol": protocol,
                "state": state,
                "service": service
            })

    return results


# -----------------------------
# 3) Socket scan validation
# -----------------------------
def socket_scan(target: str, ports):
    open_ports = []

    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)

        try:
            result = s.connect_ex((target, port))  # 0 means open
            if result == 0:
                open_ports.append(port)
        finally:
            s.close()

    return open_ports


# -----------------------------
# 4) Log results with timestamp
# -----------------------------
def log_results(target: str, nmap_data, socket_open_ports):
    logging.info(f"Target: {target}")
    logging.info(f"Nmap results count: {len(nmap_data)}")
    logging.info(f"Socket open ports count: {len(socket_open_ports)}")

    # Log Nmap parsed details
    for entry in nmap_data:
        logging.info(
            f"IP={entry['ip']} PORT={entry['port']} "
            f"PROTO={entry['protocol']} STATE={entry['state']} "
            f"SERVICE={entry['service']}"
        )

    # Log socket validation results
    logging.info(f"Socket scan open ports: {socket_open_ports}")


# -----------------------------
# 5) Optional alert logic
# -----------------------------
def check_high_risk_ports(open_ports):
    risky_ports = [23, 3389]  # Telnet, RDP
    found = [p for p in open_ports if p in risky_ports]

    if found:
        print(f"[!] ALERT: High-risk ports detected: {found}")
        logging.warning(f"High-risk ports detected: {found}")


# -----------------------------
# Main
# -----------------------------
def main():
    target = input("Enter target IP or domain: ").strip()

    print("[+] Running Nmap scan (20-1024)...")
    try:
        xml_file = run_nmap_scan(target)
    except Exception as e:
        print(f"[!] Nmap scan failed: {e}")
        return

    print("[+] Parsing Nmap XML output...")
    try:
        nmap_results = parse_nmap_xml(xml_file)
    except Exception as e:
        print(f"[!] Failed to parse XML: {e}")
        return

    # Extract open ports from Nmap results for validation
    open_ports_from_nmap = [r["port"] for r in nmap_results if r["state"] == "open" and isinstance(r["port"], int)]

    print(f"[+] Nmap found open ports: {open_ports_from_nmap}")

    print("[+] Running socket scan validation...")
    socket_open = socket_scan(target, open_ports_from_nmap)

    print(f"[+] Socket scan open ports: {socket_open}")

    print("[+] Logging results to recon_scan.log ...")
    log_results(target, nmap_results, socket_open)

    # Optional alert check
    check_high_risk_ports(socket_open)

    print("[+] Done.")


if __name__ == "__main__":
    main()
