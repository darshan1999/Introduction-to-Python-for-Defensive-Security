
# Description:
# This tool scans for ports commonly used in lateral movement (SMB, RDP, SSH).
# It helps incident responders identify potential pivot paths inside a network.
import socket

LATERAL_PORTS = {
    445: "SMB",
    3389: "RDP",
    22: "SSH"
}

def scan_for_lateral_movement(target):
    findings = []

    for port, service in LATERAL_PORTS.items():
        sock = socket.socket()
        sock.settimeout(1)

        if sock.connect_ex((target, port)) == 0:
            print(f"[!] {service} accessible on {target}:{port}")
            findings.append((port, service))

        sock.close()

    return findings


if __name__ == "__main__":
    target = input("Enter suspected host: ").strip()
    scan_for_lateral_movement(target)