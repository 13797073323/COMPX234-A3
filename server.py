import socket
import threading
import time
from collections import defaultdict

class TupleSpace:
    def __init__(self):
        self.store = dict()
        self.lock = threading.Lock()

        self.total_clients = 0
        self.total_ops = 0
        self.read_count = 0
        self.get_count = 0
        self.put_count = 0
        self.error_count = 0

    def put(self, key, value):
        with self.lock:
            if key in self.store:
                self.error_count += 1
                return "ERR", f"{key} already exists"
            else:
                self.store[key] = value
                self.put_count += 1
                self.total_ops += 1
                return "OK", f"({key}, {value}) added"

    def get(self, key):
        with self.lock:
            if key not in self.store:
                self.error_count += 1
                return "ERR", f"{key} does not exist"
            else:
                value = self.store.pop(key)
                self.get_count += 1
                self.total_ops += 1
                return "OK", f"({key}, {value}) removed"

    def read(self, key):
        with self.lock:
            if key not in self.store:
                self.error_count += 1
                return "ERR", f"{key} does not exist"
            else:
                value = self.store[key]
                self.read_count += 1
                self.total_ops += 1
                return "OK", f"({key}, {value}) read"