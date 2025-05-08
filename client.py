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

def main():
    if len(sys.argv) != 4:
        print("Usage: python client.py <hostname> <port> <request_file>")
        sys.exit(1)

    hostname = sys.argv[1]
    port = int(sys.argv[2])
    request_file = sys.argv[3]

    with open(request_file, 'r') as file:
        for line in file.readlines():
            line = line.strip()
            if line:  # Ignore empty lines
                response = send_request(hostname, port, line)
                print(f"{line}: {response}")

if __name__ == "__main__":
    main()