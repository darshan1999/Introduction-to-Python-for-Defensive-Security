# Description:
# This tool scans a range of internal IP addresses to discover active hosts and their open services.
# It helps in mapping internal network exposure during blue team assessments.
import socket

def scan_host(ip, ports):
    open_ports = []

    for port in ports:
        sock = socket.socket()
        sock.settimeout(0.5)

        if sock.connect_ex((ip, port)) == 0:
            open_ports.append(port)

        sock.close()

    return open_ports


if __name__ == "__main__":
    base_ip = input("Enter base IP (e.g., 192.168.1): ").strip()
    ports = [22, 80, 443]

    for i in range(1, 10):  # small safe range
        ip = f"{base_ip}.{i}"
        result = scan_host(ip, ports)

        if result:
            print(f"[+] {ip} → Open Ports: {result}")