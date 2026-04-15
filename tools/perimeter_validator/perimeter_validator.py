# Description:
# This tool validates external exposure by scanning critical ports on a target host.
# It helps defenders identify services that are unintentionally exposed to the internet.
import socket

def scan_ports(target, ports):
    open_ports = []

    for port in ports:
        try:
            sock = socket.socket()
            sock.settimeout(1)

            if sock.connect_ex((target, port)) == 0:
                print(f"[ALERT] {target}:{port} is OPEN (exposed externally)")
                open_ports.append(port)

            sock.close()
        except:
            pass

    return open_ports


if __name__ == "__main__":
    target = input("Enter external target: ").strip()
    critical_ports = [21, 22, 23, 80, 443, 445, 3389]

    exposed = scan_ports(target, critical_ports)

    print("\n[SUMMARY] Exposed Ports:", exposed)