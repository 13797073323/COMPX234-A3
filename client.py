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