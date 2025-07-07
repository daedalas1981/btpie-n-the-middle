import argparse
import time
import subprocess
import bluetooth
import os
from btpie.core import MITMCore
from btpie import __version__

def ensure_bluetooth_on():
    try:
        status = subprocess.check_output(["bluetoothctl", "show"], text=True)
        if "Powered: yes" in status:
            return True
        print("[!] Bluetooth is off. Enabling...")
        subprocess.run(["bluetoothctl", "power", "on"], check=True)
        return True
    except Exception as e:
        print(f"[!] Failed to enable Bluetooth: {e}")
        return False

def check_paired(mac):
    output = subprocess.getoutput(f"bluetoothctl info {mac}")
    return "Paired: yes" in output

def scan_devices():
    if not ensure_bluetooth_on():
        print("[!] Cannot scan — Bluetooth is disabled.")
        return

    print("[+] Scanning for nearby Bluetooth devices (15 seconds)...")
    devices = bluetooth.discover_devices(duration=15, lookup_names=True)

    if not devices:
        print("[!] No devices found.")
    else:
        for idx, (addr, name) in enumerate(devices):
            print(f"[{idx + 1}] {addr} - {name}")

def list_paired():
    print("\n=== Paired Devices ===")
    os.system("bluetoothctl paired-devices")
    print("======================\n")

def trust_device(mac):
    subprocess.run(["bluetoothctl", "trust", mac])
    if check_paired(mac):
        print(f"[+] Device {mac} successfully trusted and paired.")
    else:
        print(f"[!] Device {mac} trust command sent, but pairing not confirmed.")

def untrust_device(mac):
    subprocess.run(["bluetoothctl", "untrust", mac])
    print(f"[+] Device {mac} no longer trusted.")

def main():
    parser = argparse.ArgumentParser(description="BTPIE-N-THE-MIDDLE")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--scan", action="store_true", help="Scan for nearby Bluetooth devices")
    group.add_argument("--paired", action="store_true", help="List trusted/paired devices")
    group.add_argument("--trust", metavar="MAC", help="Trust a device by MAC address")
    group.add_argument("--untrust", metavar="MAC", help="Untrust/remove trust for a device by MAC address")
    group.add_argument("--mitm", action="store_true", help="Run MITM relay between master and slave")

    parser.add_argument("--master", help="Bluetooth MAC of connecting client (e.g., MotoScan)")
    parser.add_argument("--slave", help="Bluetooth MAC of target device (e.g., OBD Adapter)")
    parser.add_argument("--log", default="logs/session.log", help="Path to log file")
    parser.add_argument("--port", type=int, default=1, help="RFCOMM port to use (default: 1)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose console output")
    parser.add_argument("--version", action="store_true", help="Show BTPIE version")

    args = parser.parse_args()

    if args.version:
        print(f"BTPIE-N-THE-MIDDLE Version {__version__}")
        return

    if args.scan:
        scan_devices()
        return

    if args.paired:
        list_paired()
        return

    if args.trust:
        trust_device(args.trust)
        return

    if args.untrust:
        untrust_device(args.untrust)
        return

    if args.mitm:
        if not args.master or not args.slave:
            parser.error("[!] --master and --slave are required for MITM operation")

        if args.master == args.slave:
            confirm = input("[!] Master and Slave are the same device. Continue anyway? [y/N]: ").strip().lower()
            if confirm not in ("y", "yes"):
                print("[!] Aborting. Master and Slave must differ.")
                return

        mitm = MITMCore(
            master_mac=args.master,
            slave_mac=args.slave,
            log_file=args.log,
            port=args.port,
            verbose=args.verbose
        )
        mitm.start()

        try:
            while not mitm.stop_event.is_set():
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[!] CTRL+C received, shutting down...")
            mitm.cleanup()

if __name__ == "__main__":
    main()
