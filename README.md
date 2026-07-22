# LAN Chat CLI (`lanchat`)

Offline, LAN-only chat, installed once as a real terminal command — like `npm` or `pip`.
No internet needed. Works up to **4 devices** per room.

## One-time install (each device that will use it)

Requires Python 3.7+ (already has `pip`, which is standard with Python on Windows).

1. Copy the `lanchat-pkg` folder onto the device (or `git clone` it if you push it to a repo).
2. Open PowerShell inside the `lanchat-pkg` folder and run:
   ```powershell
   pip install .
   ```
   (use `pip install -e .` instead if you're still actively editing the code)
3. Done. Close and reopen PowerShell. Now `lanchat` works as a command from **any folder**,
   just like `python` or `npm` do — this is because `pip install` places it in Python's
   `Scripts` folder, which is on your PATH (same mechanism as any CLI tool).

Verify it worked:
```powershell
lanchat --help
```

## Usage

**Host a room** (one person does this):
```powershell
lanchat host
```
This prints a room code, e.g.:
```
Room code : P4AA-AAIV-XA
```
Share that code with your teammates (any chat app, verbally, whatever — this is just
setup info, doesn't need to be sent over your offline chat itself).

**Join a room** (everyone else, and the host too if they want to chat):
```powershell
lanchat join P4AA-AAIV-XA
```
Enter a username, then start typing. Type `/quit` to leave.

## Notes
- Max 4 devices in a room — a 5th `join` attempt gets rejected with a message.
- All devices must be on the same WiFi/router (true LAN, no internet used).
- Custom port: `lanchat host --port 6000` (room code auto-adjusts).
- If Windows Firewall prompts when you first run `lanchat host`, click **Allow** —
  otherwise other devices can't reach it.
- The "room code" is not a server-issued token — it's just the host's IP+port packed
  into a short string, decoded locally by whoever joins. No external service involved.

## Uninstall
```powershell
pip uninstall lanchat
```
