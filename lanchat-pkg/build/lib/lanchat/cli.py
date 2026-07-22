import argparse

from . import server, client


def main():
    parser = argparse.ArgumentParser(
        prog="lanchat",
        description="Offline LAN chat - host a room or join one."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    host_p = sub.add_parser("host", help="Start hosting a chat room")
    host_p.add_argument("--port", type=int, default=5555, help="Port to host on (default 5555)")

    join_p = sub.add_parser("join", help="Join an existing chat room")
    join_p.add_argument("room_code", help="Room code shown by the host")

    args = parser.parse_args()

    if args.command == "host":
        server.run(port=args.port)
    elif args.command == "join":
        client.run(args.room_code)


if __name__ == "__main__":
    main()
