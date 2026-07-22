import socket
import threading
import sys

from .roomcode import decode_room_code


def receive_messages(sock):
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                print("\n[Disconnected from server]")
                break
            print("\r" + data.decode("utf-8"), end="")
            print("You: ", end="", flush=True)
        except OSError:
            break


def run(room_code: str):
    try:
        ip, port = decode_room_code(room_code)
    except Exception:
        print(f"Invalid room code: {room_code}")
        sys.exit(1)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((ip, port))
    except (ConnectionRefusedError, OSError) as e:
        print(f"Could not connect to {ip}:{port} -> {e}")
        sys.exit(1)

    first = sock.recv(1024).decode("utf-8")

    if first.startswith("Room is full"):
        print(first)
        sock.close()
        sys.exit(1)

    print(first, end="")
    username = input()
    sock.sendall(username.encode("utf-8"))

    welcome = sock.recv(1024).decode("utf-8")
    print(welcome)

    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    try:
        while True:
            msg = input("You: ")
            if not msg:
                continue
            sock.sendall(msg.encode("utf-8"))
            if msg == "/quit":
                break
    except (KeyboardInterrupt, EOFError):
        sock.sendall(b"/quit")
    finally:
        sock.close()
