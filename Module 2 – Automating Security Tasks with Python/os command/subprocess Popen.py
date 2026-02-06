"""
Demonstrates real-time command output streaming using subprocess.Popen().

Key concepts:
- Handling long-running commands
- Streaming output line-by-line
- Process control with wait()

Defensive Security Context:
- Live monitoring of network checks
- Streaming logs or command output into detection pipelines
"""



import subprocess

process = subprocess.Popen(["ping", "-n", "5", "google.com"], stdout=subprocess.PIPE, text=True)

for line in process.stdout:
    print(">>>", line.strip())

process.wait()
