#If Nmap is unavailable or you need a quick check, Python’s socket module can scan ports directly.

"""connect_ex() returns 0 if the port is open.
We set a short timeout to avoid blocking.
You can expand this to include banner grabbing or logging.
"""


import socket

def scan_ports(target, ports):
    open_ports = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"sock {sock}")
        sock.settimeout(1)  # Short timeout for speed
        result = sock.connect_ex((target, port))  # 0 means open
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports

# Example usage
target_host = "google.com"
ports_to_test = [22, 80, 443, 8080,742]

open_found = scan_ports(target_host, ports_to_test)
print(f"Open ports on {target_host}: {open_found}")
