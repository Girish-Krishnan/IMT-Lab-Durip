import socket
from concurrent.futures import ThreadPoolExecutor

# Replace with your actual subnet
subnet = '192.168.1.'
ports_to_check = [80, 443]

def check_port(ip, port):
    try:
        with socket.create_connection((ip, port), timeout=1):
            return (ip, port, True)
    except:
        return (ip, port, False)

def scan_subnet():
    print("Scanning network...")
    ips = [subnet + str(i) for i in range(1, 255)]
    results = []

    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = []
        for ip in ips:
            for port in ports_to_check:
                futures.append(executor.submit(check_port, ip, port))

        for future in futures:
            ip, port, is_open = future.result()
            if is_open:
                results.append((ip, port))

    print("\nDevices with open web ports:")
    for ip, port in results:
        print(f"  http://{ip}:{port}" if port == 80 else f"  https://{ip}:{port}")

if __name__ == '__main__':
    scan_subnet()
