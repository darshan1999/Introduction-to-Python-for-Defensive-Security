🚨 Rogue Service Detector
Detect High-Risk Exposed Services Before Attackers Do
🛡 Overview

This tool identifies high-risk exposed services across authorized hosts by scanning for known dangerous ports and alerting when they are open.

Built as part of my “Python for Defensive Security – From Fundamentals to SOC Automation” series.

Instead of only scanning, this tool focuses on detecting potentially dangerous exposure conditions.

🚀 Features
🔍 Automated TCP SYN Scanning

Uses Nmap (-Pn -sS)

Scans critical service range (20–1024)

Explicitly scans known high-risk ports

Generates structured XML output

Uses secure subprocess execution (no shell=True)

📄 Structured XML Parsing

Parses Nmap XML using xml.etree.ElementTree

Extracts open ports per host

Converts raw scan data into structured Python objects

🗂 Multi-Host Baseline Management

Maintains a centralized rogue_service_baseline.json

Tracks exposure per host independently

Automatically adds new hosts

Supports unlimited hosts over time

🔄 Baseline Schema Migration

Detects legacy single-host baseline formats

Automatically migrates to multi-host schema

Prevents crashes due to schema evolution

🕒 Per-Host Timestamping

Stores:

last_baseline_update

Allows defenders to verify when exposure state was last trusted.

⚠ High-Risk Port Detection

Detects exposure of ports such as:

23 (Telnet – unencrypted remote access)

21 (FTP – unencrypted file transfer)

445 (SMB – lateral movement exposure)

3389 (RDP – remote desktop exposure)

5900 (VNC – remote control exposure)

Alerts are:

Printed to console

Logged to file for audit trail

🧠 How It Works

Run in baseline mode

Store current exposure state

Run in detect mode

Scan current exposure

Alert if risky services are open

🛠 Usage
Create / Update Baseline
python rogue_service_detector.py


Mode: baseline

Detect Rogue Services
python rogue_service_detector.py


Mode: detect

🎯 Defensive Use Cases

Rogue service detection

Shadow IT identification

Remote access exposure monitoring

High-risk service alerting

Audit trail logging for SOC workflows

🧰 Technologies Used

Python 3

Nmap

XML parsing (ElementTree)

JSON structured storage

Secure subprocess execution

Logging module for alerting