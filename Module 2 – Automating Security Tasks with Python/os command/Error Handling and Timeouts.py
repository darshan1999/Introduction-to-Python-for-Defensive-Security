"""
Demonstrates error handling and timeout protection for OS commands.

Key concepts:
- Preventing hung processes
- Handling command failures safely
- Using return codes and exceptions

Defensive Security Context:
- Ensures automation tools remain stable
- Critical for continuous monitoring and scheduled tasks
"""



#Example: Timeout Protection
import subprocess

try:
    subprocess.run(["sleep", "10"], timeout=3)
except subprocess.TimeoutExpired:
    print("Command timed out.")

#Example: Exit Code Checks
result = subprocess.run(["ls", "/nonexistent"], capture_output=True, text=True)

if result.returncode != 0:
    print("Error occurred:", result.stderr)