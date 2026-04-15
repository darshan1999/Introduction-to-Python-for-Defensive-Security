#Manual scanning over many ports can be slow due to timeouts. We can use threading to scan ports concurrently.

import socket
import threading

open_ports = []
lock = threading.Lock()

def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        sock.close()

        if result == 0:
            with lock:
                print(f"[+] Port {port} is open")
                open_ports.append(port)
    except:
        pass

def threaded_scan(target, ports):
    threads = []

    for port in ports:
        t = threading.Thread(target=scan_port, args=(target, port))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return open_ports

# Example usage
target = "scanme.nmap.org"
ports = range(1, 5000)

results = threaded_scan(target, ports)
print("Scan complete. Open ports:", results)


#Threading Benefits:
#Speeds up scans by running multiple checks in parallel.
#Shared data (open_ports) is protected by a lock for thread safety.