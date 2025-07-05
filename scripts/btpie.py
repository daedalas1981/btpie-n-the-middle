import argparse
import time

from btpie.core import MITMCore

def main():
    parser = argparse.ArgumentParser(description="BTPIE-N-THE-MIDDLE - Bluetooth Proxy MITM Tool")
    parser.add_argument("--target", required=True, help="Target Bluetooth MAC address (OBD device)")
    parser.add_argument("--log", default="logs/session.log", help="Path to log file")
    args = parser.parse_args()

    mitm = MITMCore(target_mac=args.target, log_file=args.log)
    mitm.start()

    try:
        while mitm.running:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] CTRL+C received, shutting down...")
        mitm.cleanup()

if __name__ == "__main__":
    main()
