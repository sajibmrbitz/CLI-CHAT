"""
Encodes an (ip, port) pair into a short, shareable room code and back.
This is purely local encoding (no internet/server involved) -- it just
packs the 4 IP bytes + 2 port bytes into a compact base32 string so
users have something nicer to share than a raw IP:port.
"""

import socket
import struct
import base64


def encode_room_code(ip: str, port: int) -> str:
    ip_bytes = socket.inet_aton(ip)          # 4 bytes
    port_bytes = struct.pack(">H", port)      # 2 bytes
    raw = ip_bytes + port_bytes
    code = base64.b32encode(raw).decode("ascii").rstrip("=")
    # group into chunks of 4 for readability: e.g. ABCD-EFGH-IJ
    grouped = "-".join(code[i:i + 4] for i in range(0, len(code), 4))
    return grouped


def decode_room_code(code: str):
    clean = code.replace("-", "").strip().upper()
    padding = "=" * ((8 - len(clean) % 8) % 8)
    raw = base64.b32decode(clean + padding)
    ip_bytes, port_bytes = raw[:4], raw[4:6]
    ip = socket.inet_ntoa(ip_bytes)
    port = struct.unpack(">H", port_bytes)[0]
    return ip, port
