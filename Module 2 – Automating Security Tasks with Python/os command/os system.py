"""
Demonstrates basic OS command execution using os.system().

Purpose:
- Execute simple system commands for quick diagnostics

Key learning:
- os.system() executes commands but does NOT capture output
- Limited error handling
- Unsafe with untrusted input

Defensive Security Context:
- Useful only for quick, trusted, one-off tasks
- Not recommended for scalable or secure automation
"""


import os
os.system("ping -c 4 google.com")