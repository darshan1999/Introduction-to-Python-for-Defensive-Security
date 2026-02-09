## Automating Reconnaissance and Scanning with Python

This module demonstrates how Python can be used to automate defensive reconnaissance tasks commonly performed in SOC and blue team environments.

### Covered Concepts
- Executing external scanners (Nmap) safely using `subprocess`
- Parsing structured Nmap XML output
- Manual TCP port scanning using Python sockets
- Validating scanner results
- Enriching reconnaissance with IP context via APIs
- Logging results with timestamps

### Scripts Included
- **Executing External Scanners (Nmap)** – Runs TCP SYN scans programmatically
- **Parsing Nmap Output (XML)** – Extracts ports, states, and services
- **Manual Port Scanning with Sockets** – Lightweight validation scanning
- **Adding IP Context with APIs** – Enriches results with metadata
- **Combining Recon and Scan** – End-to-end automated workflow

### Defensive Use Cases
- Asset discovery and exposure monitoring
- Detection of newly opened or rogue services
- Validation of vulnerability scan scope
- SOC alert enrichment and triage support

> ⚠️ All scans are intended for authorized targets only.  
> Test targets such as `scanme.nmap.org` are recommended.
