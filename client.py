import sys
import socket

def validate_request(line):
    parts = line.strip().split()
    if len(parts) < 2:
        return False, "Invalid command format"
    op = parts[0]
    if op not in ["PUT", "GET", "READ"]:
        return False, "Unknown operation"
    key = parts[1]
    value = ' '.join(parts[2:]) if len(parts) > 2 else None

    collated = f"{key} {value}" if value else key
    if len(collated) > 970:
        return False, "Collated size exceeds 970 characters"
    return True, (op, key, value)

def encode_request(op, key, value):
    cmd = {'PUT': 'P', 'GET': 'G', 'READ': 'R'}[op]
    if op == 'PUT':
        msg = f"{cmd} {key} {value}"
    else:
        msg = f"{cmd} {key}"
    msg_len = len(msg) + 4
    if msg_len < 7 or msg_len > 999:
        raise ValueError("Invalid message length")
    return f"{msg_len:03d} {msg}"

def main():
    if len(sys.argv) != 4:
        print("Usage: python client.py <hostname> <port> <request_file>")
        return
    host, port, file_path = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except IOError:
        print(f"Error: Cannot open file {file_path}")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
        except ConnectionRefusedError:
            print("Error: Server not reachable")
            return
        
        for line in lines:
            valid, result = validate_request(line)
            if not valid:
                print(f"{line.strip()}: {result}")
                continue
            op, key, value = result
            try:
                request = encode_request(op, key, value)
            except ValueError as e:
                print(f"{line.strip()}: Error - {e}")
                continue