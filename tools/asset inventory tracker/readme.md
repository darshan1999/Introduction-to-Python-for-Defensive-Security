📦 Asset Inventory Tracker
Maintain Continuous Visibility of Exposed Services
🛡 Overview

This tool automates asset exposure inventory tracking by scanning authorized hosts and maintaining a structured record of open services.

Instead of running isolated scans, it builds a persistent exposure inventory across multiple assets.

Part of my “Python for Defensive Security – From Fundamentals to SOC Automation” series.

🚀 Features
🔍 Automated TCP SYN Scanning

Uses Nmap (-Pn -sS -p 20-1024)

Structured XML output parsing

Secure subprocess execution

🗂 Structured Asset Inventory

Maintains asset_inventory.json with:

Open ports per asset

First seen timestamp

Last seen timestamp

🆕 Automatic Asset Discovery

Automatically adds new hosts

Tracks when asset was first discovered

Updates existing asset exposure state

🕒 Asset Lifecycle Tracking

Stores:

first_seen

last_seen

Enables tracking:

New assets entering environment

Asset persistence over time

🛠 Usage
python asset_inventory_tracker.py


Enter multiple targets separated by commas:

google.com, meta.com

🎯 Defensive Use Cases

Asset discovery

Exposure inventory management

Shadow IT detection

Environment visibility tracking

Service exposure auditing