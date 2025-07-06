# BTPIE-N-THE-MIDDLE

**Modern Bluetooth Proxy-In-The-Middle (MITM) Tool for Raspberry Pi**

Clean Python 3.x MITM relay with full two-way logging, device scanning, pairing management, modular design, and interactive guided setup.

---

## 🔥 Features

- Written from scratch in Python 3.x
- Compatible with latest Raspberry Pi 64-bit OS
- Classic Bluetooth (RFCOMM) relay between devices
- Full bidirectional hex-dump logging
- Device scanning, pairing list, and trust management
- Custom RFCOMM port option
- Verbose console output option
- Interactive step-by-step guided setup script
- Modular, extensible, MIT License

---

## ⚙️ Requirements

- Python 3.9+ recommended
- `pybluez` library

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage Examples

# Scan for nearby Bluetooth devices
```bash
python3 scripts/btpie.py --scan
```
# List paired/trusted devices
```bash
python3 scripts/btpie.py --paired
```
# Trust a Bluetooth device by MAC address
```bash
python3 scripts/btpie.py --trust 00:04:3E:8F:AF:1F
```
# Untrust/remove trust for a device
```bash
python3 scripts/btpie.py --untrust 00:04:3E:8F:AF:1F
```
# Run the MITM relay with full logging
```bash
python3 scripts/btpie.py --mitm --master 00:04:3E:8F:AF:1F --slave 00:02:1E:8F:AF:3F --log logs/session.log --port 1 --verbose
```
# Run interactive step-by-step setup
```bash
python3 scripts/interactive_btpie.py
```

---

## ⚙️ Arguments Table

| Flag         | Description                                           |
|--------------|-------------------------------------------------------|
| `--scan`     | Scan for nearby Bluetooth devices (discovery mode)    |
| `--paired`   | List currently paired/trusted devices                 |
| `--trust`    | Trust a device by MAC address using `bluetoothctl`    |
| `--untrust`  | Remove trust for a device by MAC address              |
| `--mitm`     | Run the MITM relay functionality                      |
| `--master`   | MAC address of the connecting client (e.g., MotoScan) |
| `--slave`    | MAC address of the target device (e.g., OBD Adapter)  |
| `--log`      | Log file path (default: `logs/session.log`)           |
| `--port`     | RFCOMM port to use (default: 1)                       |
| `--verbose`  | Enable verbose console output of hex data             |
| `--version`  | Show BTPIE version                                    |

---

## 🛠 How It Works

* Waits for master device (e.g., MotoScan) to connect
* Establishes outbound connection to slave device (e.g., OBD Adapter)
* Relays traffic in both directions, with timestamped hex-dump logging
* Supports reconnecting and only accepts trusted master devices
* Can scan and manage Bluetooth trust relationships via `bluetoothctl`
* Optional custom port and verbose modes for advanced use
* Step-by-step guided setup available for easier configuration

---

📦 Project Structure
```text
btpie-n-the-middle/
├── btpie/         # Core modules (MITM logic, adapter, logger)
├── scripts/       # CLI entry points, including interactive_btpie.py
├── tests/         # Unit tests (coming soon)
├── logs/          # Log files generated at runtime
├── requirements.txt
├── setup.py
├── README.md
```
---

🧭 Roadmap

* Socket timeouts for better stability (implemented)
* Automatic reconnect logic for both master/slave sides (implemented)
* BLE support (future)
* Interactive device selector menu (partially implemented)
* Enhanced logging with traffic summaries

---

## 🔗 Related Projects

This project was inspired by the concept of Bluetooth Proxy-in-the-Middle tools like [btproxy by conorpp](https://github.com/conorpp/btproxy), but was built entirely from scratch in Python 3 with modern design, improved stability, and added features.

---

## 📄 License

MIT License — see LICENSE file for full details.

---
Built by Robert Cole as a clean, modern alternative to legacy btproxy tools.
