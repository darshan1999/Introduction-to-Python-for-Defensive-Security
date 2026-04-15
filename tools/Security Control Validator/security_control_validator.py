# Description:
# This tool verifies whether security controls (e.g., firewall rules) are properly enforced.
# It checks if restricted ports are incorrectly exposed.
import socket


EXPECTED_BLOCKED = [23, 21, 445]  # ports that should NOT be open

def validate_controls(target):
    violations = []

    for port in EXPECTED_BLOCKED:
        sock = socket.socket()
        sock.settimeout(1)

        if sock.connect_ex((target, port)) == 0:
            print(f"[FAIL] Port {port} should be BLOCKED but is OPEN")
            violations.append(port)

        sock.close()

    if not violations:
        print("[PASS] All security controls are properly enforced")

    return violations


if __name__ == "__main__":
    target = input("Enter target: ").strip()
    validate_controls(target)