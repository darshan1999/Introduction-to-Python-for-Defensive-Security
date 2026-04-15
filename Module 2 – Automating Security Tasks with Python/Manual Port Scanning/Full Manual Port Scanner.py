#We can now expand the logic into a full scanner that tests multiple ports and handles common edge cases.

#Basic Multi-Port Scanner:
import socket

def scan_ports(target, port_list, timeout=1):
    open_ports = []

    for port in port_list:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)

            result = sock.connect_ex((target, port))

            if result == 0:
                print(f"[+] Port {port} is open")
                open_ports.append(port)
            else:
                print(f"[-] Port {port} is closed or filtered")

            sock.close()

        except Exception as e:
            print(f"[!] Error scanning port {port}: {e}")

    return open_ports

# Example usage
target_host = "scanme.nmap.org"
ports_to_scan = list(range(20, 30))  # Common ports

found_ports = scan_ports(target_host, ports_to_scan)
print("Open ports found:", found_ports)

#Explanation:
#Loops through a list of ports.
#Each port is tested individually using a short-lived TCP socket.
#Results are appended to a list for later use or reporting.