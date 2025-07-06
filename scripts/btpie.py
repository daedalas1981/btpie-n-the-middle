import argparse
import time
import bluetooth
import os
from btpie.core import MITMCore
from btpie import __version__

def scan_devices():
    devices = bluetooth.discover_devices(duration=8, lookup_names=True)
    for addr, name in devices:
        print(f"{addr} - {name}")

def list_paired():
    os.system("bluetoothctl paired-devices")

def trust_device(mac):
    os.system(f"bluetoothctl trust {mac}")

def untrust_device(mac):
    os.system(f"bluetoothctl untrust {mac}")

def main():
    parser = argparse.ArgumentParser(description="BTPIE-N-THE-MIDDLE")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--scan", action="store_true", help="Scan for nearby Bluetooth devices")
    group.add_argument("--paired", action="store_true", help="List trusted/paired devices")
    group.add_argument("--trust", metavar="MAC", help="Trust a device by MAC address")
    group.add_argument("--untrust", metavar="MAC", help="Untrust/remove trust for a device by MAC address")
    group.add_argument("--mitm", action="store_true", help="Run MITM relay between master and slave")

    parser.add_argument("--master", help="Bluetooth MAC of connecting client (e.g., MotoScan)")
    parser.add_argument("--slave", help="Bluetooth MAC of target device (e.g., OBD)")
    parser.add_argument("--log", default="logs/session.log", help="Path to log file")
    parser.add_argument("--port", type=int, default=1, help="RFCOMM port to use (default: 1)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose console output")
    parser.add_argument("--version", action="store_true", help="Show tool version")

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
