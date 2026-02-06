"""
Demonstrates secure command execution using subprocess.run().

Key concepts:
- Capturing stdout and stderr
- Checking exit codes
- Timeout handling
- Safer alternative to os.system()

Defensive Security Context:
- Core method for automating diagnostics
- Enables structured parsing and reporting in SOC tools
"""


import subprocess

result = subprocess.run(["ping", "-c", "4", "8.8.8.8"], capture_output=True, text=True)

print("Exit Code:", result.returncode)
print("Output:", result.stdout)
print("Errors:", result.stderr)
