# IP Kill-Switch

A simple Python script that periodically checks the machine's public IP address. If it differs from a specific target IP (e.g. your VPN/proxy IP) — or if it can't be checked at all — the script automatically closes browsers (and optionally other apps) to prevent your real IP from leaking.

## Features

- Periodic public IP check with a configurable interval
- Automatically closes a configurable list of processes (browsers, VS Code, etc.) when the IP changes
- **Fail-safe** behavior: if the IP check fails repeatedly (e.g. no internet at all), it's treated the same as an IP change
- No background service or complex setup — just a single Python script

## Requirements

- Python 3.10+
- `requests` and `psutil` packages

```bash
pip install requests psutil
```

## Installation & Usage

```bash
git clone https://github.com/<username>/<repo-name>.git
cd <repo-name>
pip install -r requirements.txt
python ip_killswitch.py
```

Stop it with `Ctrl+C`.

## Configuration

All settings are at the top of `ip_killswitch.py`:

| Variable | Description | Default |
|---|---|---|
| `TARGET_IP` | The IP the machine is expected to always have | `82.115.17.77` |
| `CHECK_INTERVAL` | Time between checks (seconds) | `0.5` |
| `FAIL_THRESHOLD` | Consecutive failed IP checks before closing processes | `2` |
| `BROWSER_PROCESS_NAMES` | List of process names to kill on an IP leak | common browsers + VS Code |

Example — adding another app to the kill list:

```python
BROWSER_PROCESS_NAMES = [
    "chrome.exe",
    "msedge.exe",
    "firefox.exe",
    "Code.exe",
    "telegram.exe",   # example custom app
]
```

## Notes

- This script only **kills processes** — it doesn't control network/firewall level traffic. For a more reliable kill switch, also use your VPN client's built-in Kill Switch feature or Windows Firewall rules.
- Closing some processes (especially ones running with elevated privileges) may require running the script as **Administrator**.
- Currently tested on Windows only (process names use the `.exe` suffix). For Linux/macOS, adjust the names in `BROWSER_PROCESS_NAMES` accordingly.

## License

MIT — free to use, modify, and distribute.
