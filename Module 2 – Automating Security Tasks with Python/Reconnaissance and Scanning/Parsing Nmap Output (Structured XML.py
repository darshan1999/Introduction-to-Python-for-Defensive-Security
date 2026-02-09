#Nmap supports structured output via the -oX flag, which is ideal for automation.
"""Explanation:
ElementTree parses the XML into nested Python objects.
We extract the host IP and loop over each port.
This allows structured reporting and integration with dashboards or alerts."""

#Step 1: Run the scan and save XML
#nmap -p 22,80,443 -Pn scanme.nmap.org -oX output.xml

#Step 2: Parse the XML with xml.etree.ElementTree
import xml.etree.ElementTree as ET

# Load and parse the XML file
tree = ET.parse("output.xml")
root = tree.getroot()

# Iterate over host blocks
for host in root.findall("host"):
    ip = host.find("address").get("addr")
    print(f"Host: {ip}")

    # Get open ports
    for port in host.findall("ports/port"):
        port_id = port.get("portid")
        protocol = port.get("protocol")
        state = port.find("state").get("state")
        service = port.find("service").get("name", "unknown")
        print(f" - Port {port_id}/{protocol}: {state} ({service})")

