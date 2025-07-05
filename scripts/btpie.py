import argparse
import time
import bluetooth
import os
from btpie.core import MITMCore

def scan_devices():
    print("[*] Scanning for nearby Bluetooth devices (8 seconds)...")
    devices = bluetooth.discover_devices(duration=8, lookup_names=True)
    if not devices:
        print("[!] No devices found.")
    else:
        for addr, name in devices:
            print(f"    {addr} - {name}")

def list_paired_devices():
    print("[*] Listing paired devices:")
    os.system("bluetoothctl paired-devices")

def trust_device(mac):
    print(f"[*] Trusting device {mac}")
    os.system(f"bluetoothctl trust {mac}")

def main():
    parser = argparse.ArgumentParser(description="BTPIE-N-THE-MIDDLE - Bluetooth Proxy MITM Tool")

    parser.add_argument("--scan", action="store_true", help="Scan for nearby Bluetooth devices")
    parser.add_argument("--paired", action="store_true", help="List paired/trusted devices")
    parser.add_argument("--trust", metavar="MAC", help="Trust a Bluetooth device by MAC address")

    parser.add_argument("--master", help="Bluetooth MAC of the connecting device (e.g., MotoScan)")
    parser.add_argument("--slave", help="Bluetooth MAC of the target device (e.g., OBD Adapter)")
    parser.add_argument("--log", default="logs/session.log", help="Path to log file")

    args = parser.parse_args()

    # Handle scan/paired/trust options
    if args.scan:
        scan_devices()
        return

    if args.paired:
        list_paired_devices()
        return

    if args.trust:
        trust_device(args.trust)
        return

    # Validate MITM requirements
    if not args.master or not args.slave:
        parser.error("[!] You must provide both --master and --slave for MITM operation.")

    # Start MITM relay
    mitm = MITMCore(master_mac=args.master, slave_mac=args.slave, log_file=args.log)
    mitm.start()

    try:
        while mitm.running:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] CTRL+C received, shutting down...")
        mitm.cleanup()

if __name__ == "__main__":
    main()
