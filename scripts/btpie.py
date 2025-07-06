btpie_script = """import argparse
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

def main():
    parser = argparse.ArgumentParser(description="BTPIE-N-THE-MIDDLE")
    parser.add_argument("--scan", action="store_true")
    parser.add_argument("--paired", action="store_true")
    parser.add_argument("--trust")
    parser.add_argument("--master")
    parser.add_argument("--slave")
    parser.add_argument("--log", default="logs/session.log")
    parser.add_argument("--version", action="store_true")
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

    if not args.master or not args.slave:
        parser.error("[!] --master and --slave are required for MITM operation")

    mitm = MITMCore(args.master, args.slave, args.log)
    mitm.start()

    try:
        while mitm.running:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] CTRL+C received, shutting down...")
        mitm.cleanup()

if __name__ == "__main__":
    main()
