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