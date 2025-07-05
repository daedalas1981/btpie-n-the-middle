import argparse
import time
from btpie.core import MITMCore

def main():
    parser = argparse.ArgumentParser(description="BTPIE-N-THE-MIDDLE - Bluetooth Proxy MITM Tool")

    parser.add_argument("--master", required=True, help="Bluetooth MAC of the connecting device (e.g., MotoScan)")
    parser.add_argument("--slave", required=True, help="Bluetooth MAC of the target device (e.g., OBD Adapter)")
    parser.add_argument("--log", default="logs/session.log", help="Path to log file")

    args = parser.parse_args()

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
