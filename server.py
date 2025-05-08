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

    def get_stats(self):
        with self.lock:
            num_tuples = len(self.store)
            avg_key = sum(len(k) for k in self.store.keys()) / num_tuples if num_tuples > 0 else 0
            avg_value = sum(len(v) for v in self.store.values()) / num_tuples if num_tuples > 0 else 0
            avg_tuple = avg_key + avg_value if num_tuples > 0 else 0
            return (
                num_tuples,
                avg_tuple,
                avg_key,
                avg_value,
                self.total_clients,
                self.total_ops,
                self.read_count,
                self.get_count,
                self.put_count,
                self.error_count
            )

class ThreadedTCPServer(socket.ThreadingMixIn, socket.socket):
    pass

def handle_client(conn, addr, tuple_space):
    tuple_space.total_clients += 1
    try:
        while True:
            data = conn.recv(1024).decode().strip()
            if not data:
                break

            msg_len = int(data[:3])
            cmd = data[4]
            parts = data[5:].split(' ', 1)
            key = parts[0]
            value = parts[1] if len(parts) > 1 else None


            if cmd == 'P':
                status, detail = tuple_space.put(key, value)
            elif cmd == 'G':
                status, detail = tuple_space.get(key)
            elif cmd == 'R':
                status, detail = tuple_space.read(key)
            else:
                status, detail = "ERR", "invalid command"


            response = f"{status} {detail}"
            response_len = f"{len(response) + 4:03d}"
            full_response = f"{response_len} {response}"
            conn.sendall(full_response.encode())
    except Exception as e:
        print(f"Client {addr} error: {e}")
    finally:
        conn.close()

def print_stats(tuple_space):
    while True:
        time.sleep(10)
        stats = tuple_space.get_stats()
        print(f"[STAT] Tuples={stats[0]} | AvgSize={stats[1]:.2f} | Clients={stats[4]} | Ops={stats[5]} (R:{stats[6]} G:{stats[7]} P:{stats[8]}) | Errors={stats[9]}")

if __name__ == "__main__":
    HOST, PORT = "localhost", 51234
    tuple_space = TupleSpace()

    stat_thread = threading.Thread(target=print_stats, args=(tuple_space,), daemon=True)
    stat_thread.start()

    with ThreadedTCPServer(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr, tuple_space))
            client_thread.start()