🔎 Change Monitoring Tool
Detect Exposure Drift Before Attackers Do
🛡 Overview

This tool monitors service exposure changes across hosts by comparing current scan results against a trusted baseline.

Instead of running one-off scans, it detects exposure drift over time.

Designed as part of my “Python for Defensive Security – From Fundamentals to SOC Automation” series.

🚀 Features
🔍 Automated TCP SYN Scanning

Uses Nmap (-Pn -sS -p 20-1024)

Structured XML output per host

Secure subprocess execution (no shell=True)

📄 XML-Based Parsing

Parses Nmap XML using xml.etree.ElementTree

Extracts open ports per host

Converts scan data into structured Python objects

🗂 Multi-Host Baseline Management

Maintains a single change_monitor_baseline.json

Tracks exposure independently per host

Automatically adds new hosts

Supports unlimited hosts over time

🔄 Baseline Schema Migration

Detects legacy single-host baseline format

Automatically converts to multi-host format

Prevents schema-related crashes

🕒 Per-Host Timestamping

Stores:

last_baseline_update

Allows defenders to verify:

When exposure state was last trusted

⚖ Exposure Drift Detection

Identifies:

Newly opened ports

Closed ports

Unchanged ports

Enables:

Configuration drift detection

Unexpected service exposure detection

Change validation across scans

🧠 How It Works

Run scan in baseline mode

Tool stores trusted exposure state

Run later in compare mode

Tool detects exposure changes

🛠 Usage
Create / Update Baseline
python change_monitoring_tool.py


Mode: baseline

Detect Exposure Drift
python change_monitoring_tool.py


Mode: compare

🎯 Defensive Use Cases

Exposure drift monitoring

Rogue service detection

Asset exposure tracking

Infrastructure change auditing

Early misconfiguration detection

🧰 Technologies Used

Python 3

Nmap

XML parsing (ElementTree)

JSON structured storage

Secure subprocess execution