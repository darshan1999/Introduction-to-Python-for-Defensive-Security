#Python’s built-in socket module provides an interface to the BSD socket API. It allows you to:

#Create TCP or UDP connections
#Send and receive raw data
#Handle timeouts and connection exceptions
#Basic TCP Socket Example:
import socket

# Create a TCP socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set timeout to avoid hanging on unresponsive hosts
sock.settimeout(2)

# Try connecting to a host and port
result = sock.connect_ex(("example.com", 80))

if result == 0:
    print("Port 80 is open")
else:
    print("Port 80 is closed or filtered")

sock.close()
#Explanation:
#socket.AF_INET defines the IPv4 address family.
#socket.SOCK_STREAM creates a TCP connection.
#connect_ex() attempts to connect and returns 0 on success or an error code.
#Timeouts prevent scripts from hanging indefinitely.