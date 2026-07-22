import socket
import threading
import sys
from datetime import datetime

from .roomcode import encode_room_code

MAX_DEVICES = 4

clients = {}   # socket -> username
clients_lock = threading.Lock()


def timestamp():
    return datetime.now().strftime("%H:%M:%S")


def broadcast(message, sender_socket=None):
    with clients_lock:
        dead = []
        for sock in clients:
            if sock is sender_socket:
                continue
            try:
                sock.sendall(message.encode("utf-8"))
            except OSError:
                dead.append(sock)
        for sock in dead:
            _drop(sock)


def _drop(sock):
    name = clients.pop(sock, None)
    try:
        sock.close()
    except OSError:
        pass
    return name


def remove_client(sock):
    with clients_lock:
        name = _drop(sock)
    if name:
        print(f"[{timestamp()}] {name} disconnected.")
        broadcast(f"[{timestamp()}] * {name} left the chat *\n")


def handle_client(sock, addr):
    try:
        with clients_lock:
            full = len(clients) >= MAX_DEVICES
        if full:
            sock.sendall(b"Room is full (max 4 devices). Try again later.\n")
            sock.close()
            return

        sock.sendall(b"Enter your username: ")
        username = sock.recv(1024).decode("utf-8").strip()
        if not username:
            username = f"Guest-{addr[1]}"

        with clients_lock:
            clients[sock] = username

        print(f"[{timestamp()}] {username} connected from {addr[0]}")
        broadcast(f"[{timestamp()}] * {username} joined the chat *\n", sender_socket=sock)
        sock.sendall(f"Connected as {username}. Type /quit to leave.\n".encode("utf-8"))

        while True:
            data = sock.recv(4096)
            if not data:
                break
            text = data.decode("utf-8").strip()
            if not text:
                continue
            if text == "/quit":
                break
            print(f"[{timestamp()}] {username}: {text}")
            broadcast(f"[{timestamp()}] {username}: {text}\n", sender_socket=sock)
    except (ConnectionResetError, OSError):
        pass
    finally:
        remove_client(sock)


def run(port: int = 5555):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen()

    lan_ip = socket.gethostbyname(socket.gethostname())
    room_code = encode_room_code(lan_ip, port)

    print("=" * 55)
    print(" LAN CHAT - hosting room")
    print(f" Room code : {room_code}")
    print(f" (or share directly -> IP: {lan_ip}  Port: {port})")
    print(f" Max devices: {MAX_DEVICES}")
    print(" Everyone must be on the same WiFi/LAN. No internet needed.")
    print(" Share this room code with your partners:")
    print(f"     lanchat join {room_code}")
    print("=" * 55)

    try:
        while True:
            client_sock, addr = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_sock, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        with clients_lock:
            for sock in list(clients):
                sock.close()
        server_socket.close()
        sys.exit(0)
