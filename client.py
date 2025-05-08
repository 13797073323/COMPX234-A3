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
    msg_len = len(msg) + 4  # 3位长度 + 空格
    if msg_len < 7 or msg_len > 999:
        raise ValueError("Invalid message length")
    return f"{msg_len:03d} {msg}"