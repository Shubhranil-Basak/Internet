import subprocess
import time
import os

BASE_DIR = os.path.dirname(__file__)
TLD_DIR = os.path.join(BASE_DIR, "servers", "tld")
AUTH_DIR = os.path.join(BASE_DIR, "servers", "auth")

def list_modules(folder, prefix):
    modules = []
    for file in os.listdir(folder):
        if file.endswith(".py") and file != "__init__.py":
            name = file[:-3]  # remove .py
            modules.append(f"{prefix}.{name}")
    return modules

def start_server(module):
    print(f"Starting {module}")
    return subprocess.Popen(["python", "-m", module])

processes = []

try:
    # Start root DNS
    processes.append(start_server("dns.servers.root"))

    # Start all TLD servers
    for mod in list_modules(TLD_DIR, "dns.servers.tld"):
        processes.append(start_server(mod))
        time.sleep(0.2)

    # Start all authoritative servers
    for mod in list_modules(AUTH_DIR, "dns.servers.auth"):
        processes.append(start_server(mod))
        time.sleep(0.2)

    # Wait for all
    for p in processes:
        p.wait()

except KeyboardInterrupt:
    print("\nShutting down all DNS servers...")
    for p in processes:
        p.terminate()
