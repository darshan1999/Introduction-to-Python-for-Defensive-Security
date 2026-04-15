#Some services respond with metadata (e.g., a web server header). We can connect and read the initial response to identify the service.

def grab_banner(ip, port):
    try:
        s = socket.socket()
        s.settimeout(2)
        s.connect((ip, port))
        banner = s.recv(1024)
        s.close()
        return banner.decode(errors='ignore')
    except:
        return None

# Use banner grabbing after confirming port is open
ip = "scanme.nmap.org"
for port in [21, 22, 80]:
    banner = grab_banner(ip, port)
    if banner:
        print(f"Banner from port {port}:\n{banner}")


#Use Cases:
#Identify service versions (Apache, SSH, etc.)
#Detect honeypots or fake services
#Enrich vulnerability scans with context