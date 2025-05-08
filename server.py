import socket
import threading
import time


tuple_space = {}
lock = threading.Lock()


def handle_client(client_socket):
    while True:
        try:

            request = client_socket.recv(1024).decode()
            if not request:
                break

            print(f"Received: {request}")
            response = process_request(request)
            client_socket.send(response.encode())
        except Exception as e:
            print(f"Error: {e}")
            break

    client_socket.close()

