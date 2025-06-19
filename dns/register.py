import json
import os
import utils

ZONES_PATH = os.path.join("dns", "zones")
AUTH_PATH = os.path.join("dns", "servers", "auth")
TLD_PATH = os.path.join("dns", "servers", "tld")

os.makedirs(ZONES_PATH, exist_ok=True)
os.makedirs(AUTH_PATH, exist_ok=True)
os.makedirs(TLD_PATH, exist_ok=True)

def load_zone(file_name):
    path = os.path.join(ZONES_PATH, file_name)
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def save_zone(file_name, data):
    path = os.path.join(ZONES_PATH, file_name)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def ensure_zone_file(file_name):
    path = os.path.join(ZONES_PATH, file_name)
    if not os.path.exists(path):
        save_zone(file_name, {})

def make_server_file(name, port, folder, zone_file):
    filename = os.path.join(folder, f"{name}.py")
    if os.path.exists(filename):
        return

    content = f'''from dns.core import DNSServer

if __name__ == "__main__":
    server = DNSServer("dns/zones/{zone_file}", port={port})
    server.start()
'''
    with open(filename, "w") as f:
        f.write(content)
    print(f"🛠️ Created DNS server script: {filename}")

def register_domain(domain, ip):
    parts = domain.split(".")
    if len(parts) < 2:
        print("❌ Invalid domain. Must include TLD (e.g. example.com)")
        return

    tld = parts[-1]
    tld_zone_file = f"{tld}.json"
    root_zone = load_zone("root.json")
    tld_zone = load_zone(tld_zone_file)

    # Step 1: Ensure TLD is in root
    if tld not in root_zone:
        tld_port = utils.get_next_free_port()
        root_zone[tld] = {"forward": ["localhost", tld_port]}
        save_zone("root.json", root_zone)
        print(f"🛠️ Added TLD .{tld} to root zone on port {tld_port}")

    # Step 2: Identify base domain
    base_domain = ".".join(parts[-2:])
    subdomain = domain if domain != base_domain else None

    # Step 3: Ensure base domain is delegated in TLD
    if base_domain not in tld_zone:
        auth_port = utils.get_next_free_port()
        tld_zone[base_domain] = {"forward": ["localhost", auth_port]}
        save_zone(tld_zone_file, tld_zone)
        print(f"🛠️ Delegated {base_domain} under .{tld} on port {auth_port}")

    # Step 4: Create TLD and Auth server scripts
    if not os.path.exists(os.path.join(TLD_PATH, f"{tld}.py")):
        make_server_file(tld, tld_port, TLD_PATH, tld_zone_file)

    auth_script_name = base_domain.replace(".", "_")
    auth_zone_file = f"{base_domain}.json"
    if not os.path.exists(os.path.join(AUTH_PATH, f"{auth_script_name}.py")):
        make_server_file(auth_script_name, auth_port, AUTH_PATH, auth_zone_file)

    # Step 5: Load and check zone data
    ensure_zone_file(auth_zone_file)
    zone_data = load_zone(auth_zone_file)

    if domain in zone_data:
        print(f"⚠️ {domain} already registered.")
        return

    if ip in zone_data:
        existing_domain = zone_data[ip].get("ip")
        print(f"❌ IP {ip} is already assigned to {existing_domain}.")
        return

    # Step 6: Add forward and reverse entries
    zone_data[domain] = {"ip": ip}
    zone_data[ip] = {"ip": domain}
    save_zone(auth_zone_file, zone_data)

    if subdomain:
        print(f"✅ Registered subdomain {domain} → {ip}")
    else:
        print(f"✅ Registered domain {domain} → {ip}")



def main():
    print("🌐 Domain Registration CLI")
    domain = input("Enter domain (e.g. example.com): ").strip()
    ip = input("Enter IP address: ").strip()
    register_domain(domain, ip)

if __name__ == "__main__":
    main()
