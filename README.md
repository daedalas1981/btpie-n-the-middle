# BTPIE-N-THE-MIDDLE

**Modern Bluetooth Proxy-In-The-Middle (MITM) Tool for Raspberry Pi**

Clean Python 3.x MITM relay with full two-way logging, device scanning, pairing management, and modular design.

---

## 🔥 Features

- Written from scratch in Python 3.x
- Compatible with latest Raspberry Pi 64-bit OS
- Classic Bluetooth (RFCOMM) relay between devices
- Full bidirectional hex-dump logging
- Device scanning, pairing list, and trust management
- Modular, extensible, MIT License

---

## ⚙️ Requirements

- Python 3.9+ recommended
- `pybluez` library

Install dependencies:

```bash
pip install -r requirements.txt


🚀 Usage Examples

# Scan for nearby Bluetooth devices
python3 scripts/btpie.py --scan

# List paired/trusted devices
python3 scripts/btpie.py --paired

# Trust a Bluetooth device by MAC address
python3 scripts/btpie.py --trust 00:04:3E:8F:AF:1F

# Run the MITM relay with full logging
python3 scripts/btpie.py --master 00:04:3E:8F:AF:1F --slave 00:02:1E:8F:AF:3F --log logs/session.log


⚙️ Arguments Table

| Flag       | Description                                           |
| ---------- | ----------------------------------------------------- |
| `--scan`   | Scan for nearby Bluetooth devices (discovery mode)    |
| `--paired` | List currently paired/trusted devices                 |
| `--trust`  | Trust a device by MAC address using `bluetoothctl`    |
| `--master` | MAC address of the connecting client (e.g., MotoScan) |
| `--slave`  | MAC address of the target device (e.g., OBD Adapter)  |
| `--log`    | Log file path (default: `logs/session.log`)           |


🛠 How It Works

Waits for master device (e.g., MotoScan) to connect

Establishes outbound connection to slave device (e.g., OBD Adapter)

Relays traffic in both directions, with timestamped hex-dump logging

Supports reconnecting and only accepts trusted master devices

Can scan and manage Bluetooth trust relationships via bluetoothctl

📦 Project Structure

btpie-n-the-middle/
├── btpie/         # Core modules (MITM logic, adapter, logger)
├── scripts/       # CLI entry point
├── tests/         # Unit tests (coming soon)
├── logs/          # Log files generated at runtime
├── requirements.txt
├── setup.py
├── README.md

🧭 Roadmap

Socket timeouts for better stability

Automatic reconnect logic for both master/slave sides

BLE support (future)

Interactive device selector menu

Enhanced logging with traffic summaries

📄 License

MIT License — see LICENSE file for full details.

Built by Robert Cole as a clean, modern alternative to legacy btproxy tools.




