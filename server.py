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


def process_request(request):
    parts = request.split()
    if len(parts) < 2:
        return "ERR Invalid request"

    command = parts[1]

    if command == 'R':  # READ
        key = parts[2]
        return read_tuple(key)
    elif command == 'G':  # GET
        key = parts[2]
        return get_tuple(key)
    elif command == 'P':  # PUT
        key = parts[2]
        value = ' '.join(parts[3:])
        return put_tuple(key, value)
    else:
        return "ERR Unknown command"

def read_tuple(key):
    with lock:
        if key in tuple_space:
            value = tuple_space[key]
            return f"OK ({key}, {value}) read"
        else:
            return f"ERR {key} does not exist"

def get_tuple(key):
    with lock:
        if key in tuple_space:
            value = tuple_space.pop(key)
            return f"OK ({key}, {value}) removed"
        else:
            return f"ERR {key} does not exist"

def put_tuple(key, value):
    with lock:
        if key not in tuple_space:
            tuple_space[key] = value
            return f"OK ({key}, {value}) added"
        else:
            return f"ERR {key} already exists"


def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)

    print(f"Server listening on port {port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")

        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    start_server(51234)