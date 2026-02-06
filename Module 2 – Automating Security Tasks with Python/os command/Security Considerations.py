"""
Demonstrates secure vs insecure command execution patterns.

Key concepts:
- Avoiding shell injection
- Validating user input
- Safe usage of subprocess

Defensive Security Context:
- Prevents command injection vulnerabilities
- Reinforces secure coding practices in automation
"""




#Avoid Shell Injection
#Bad practice (dangerous with user input):

subprocess.run(f"ping {user_input}", shell=True)
#Preferred:

subprocess.run(["ping", user_input])
#Always validate input (IP/domain formats)
#Never pass unchecked user data to shell=True
#Avoid using shell=True unless required by syntax (e.g., redirection, pipes)