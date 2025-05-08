import socket
import sys


def send_request(hostname, port, request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((hostname, port))

        # Send the request to the server
        sock.sendall(request.encode())

        # Receive the response from the server
        response = sock.recv(1024).decode()

    return response
