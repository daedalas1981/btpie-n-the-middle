import subprocess
import time
import bluetooth
from btpie.core import MITMCore

def scan_devices(role, duration=15):
    print(f"[+] Scanning for {role.upper()} device ({duration} seconds)...")
    devices = bluetooth.discover_devices(duration=duration, lookup_names=True)

    if not devices:
        print(f"[!] No {role} devices found.")
    else:
        for idx, (addr, name) in enumerate(devices):
            print(f"[{idx + 1}] {addr} - {name}")

    return devices

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

def trust_device(mac):
    subprocess.run(["bluetoothctl", "trust", mac])

def show_paired_devices():
    print("\n=== Paired Devices ===")
    subprocess.run(["bluetoothctl", "paired-devices"])
    print("======================\n")

def pairing_instructions(role, mac):
    print(f"\n[!] {role.capitalize()} device {mac} is not paired.\n")
    print("To pair the device, run the following:")
    print("$ bluetoothctl")
    print("> discoverable on" if role == "master" else "> agent on")
    print("> pair", mac)
    print("> trust", mac)
    print("> exit\n")
    print("After pairing, restart this setup.\n")

def select_device(role):
    view_paired = input("View already paired devices? [Y/n]: ").strip().lower()
    if view_paired in ("y", "yes", ""):
        show_paired_devices()

    while True:
        scan_time = input(f"Scan duration for {role} in seconds [default 15]: ").strip()
        scan_time = int(scan_time) if scan_time.isdigit() else 15

        devices = scan_devices(role, duration=scan_time)
        if not devices:
            retry = input(f"No {role} devices found. Retry scan? [Y/n]: ").strip().lower()
            if retry not in ("", "y", "yes"):
                return None
            continue

        try:
            selection = int(input(f"Select {role.capitalize()} by Number: ")) - 1
            selected_mac = devices[selection][0]
            return selected_mac
        except (IndexError, ValueError):
            print("[!] Invalid selection. Try again.")

def interactive_setup():
    print("\n=== BTPIE-N-THE-MIDDLE Interactive Setup ===\n")

    if not ensure_bluetooth_on():
        print("[!] Bluetooth unavailable. Exiting.")
        return

    run_mitm = input("Run BTPie? [Y/n]: ").strip().lower()
    if run_mitm not in ("y", "yes", ""):
        print("Exiting...")
        return

    master_mac = select_device("master")
    if not master_mac:
        return

    if not check_paired(master_mac):
        pairing_instructions("master", master_mac)
        return

    slave_mac = select_device("slave")
    if not slave_mac:
        return

    if master_mac == slave_mac:
        confirm = input("[!] Master and Slave are the same device. Continue anyway? [y/N]: ").strip().lower()
        if confirm not in ("y", "yes"):
            print("Restarting selection...")
            return interactive_setup()

    if not check_paired(slave_mac):
        pairing_instructions("slave", slave_mac)
        return

    use_log = input("Log to file? [Y/n]: ").strip().lower()
    log_file = "logs/session.log" if use_log in ("y", "yes", "") else None

    if log_file:
        custom_name = input("Log Name? (press Enter to use default): ").strip()
        if custom_name:
            log_file = f"logs/{custom_name}.log"

    debug = input("Debug Mode? [Y/n]: ").strip().lower() in ("y", "yes", "")
    verbose = input("Verbose Output? [Y/n]: ").strip().lower() in ("y", "yes", "")
    port = 1  # Static for now; can prompt if desired

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
