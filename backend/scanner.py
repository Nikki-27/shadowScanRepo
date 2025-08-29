import socket
import ipaddress
import asyncio

# --- Profiles ---
SCAN_PROFILES = {
    "quick": [22, 80, 443],
    "medium": [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080],
    "full": list(range(1, 1025)),
}

# --- TCP Scan ---
async def tcp_scan(ip, port, timeout, verbose):
    result = {"ip": ip, "port": port, "protocol": "TCP", "status": "closed"}
    try:
        conn = asyncio.open_connection(ip, port)
        reader, writer = await asyncio.wait_for(conn, timeout=timeout)

        # mark open
        result["status"] = "open"
        result["service"] = socket.getservbyport(port, "tcp") if port < 1024 else "unknown"

        # banner grabbing
        try:
            writer.write(b"\r\n")
            await writer.drain()
            banner = await asyncio.wait_for(reader.read(100), timeout=1)
            result["banner"] = banner.decode(errors="ignore").strip()
        except:
            result["banner"] = None

        writer.close()
        await writer.wait_closed()
    except:
        if verbose:
            result["status"] = "closed"   # keep closed entries in verbose mode
        else:
            return None
    return result

# --- UDP Scan ---
async def udp_scan(ip, port, timeout, verbose):
    result = {"ip": ip, "port": port, "protocol": "UDP", "status": "closed"}
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        sock.sendto(b"\x00", (ip, port))
        try:
            data, _ = sock.recvfrom(1024)
            result["status"] = "open"
            result["banner"] = data.decode(errors="ignore").strip()
        except socket.timeout:
            if verbose:
                result["status"] = "closed"
            else:
                return None
        result["service"] = socket.getservbyport(port, "udp") if port < 1024 else "unknown"
    except:
        if not verbose:
            return None
    return result

# --- Handle CIDR expansion ---
def expand_targets(targets):
    expanded = []
    for target in targets:
        try:
            net = ipaddress.ip_network(target, strict=False)
            expanded.extend([str(ip) for ip in net.hosts()])
        except ValueError:
            expanded.append(target)
    return expanded

# --- Main scanning ---
async def scan_targets(request):
    tasks = []
    targets = expand_targets(request.targets)

    # select ports
    if isinstance(request.ports, list):
        ports = request.ports
    elif isinstance(request.ports, int):
        ports = list(range(1, request.ports + 1))
    else:
        ports = SCAN_PROFILES.get(request.profile, [80, 443])

    # schedule tasks
    for ip in targets:
        for port in ports:
            if request.udp:
                tasks.append(udp_scan(ip, port, request.timeout, request.verbose))
            else:
                tasks.append(tcp_scan(ip, port, request.timeout, request.verbose))

    results = await asyncio.gather(*tasks)
    # filter Nones
    results = [r for r in results if r]

    # group by IP
    grouped = {}
    for r in results:
        grouped.setdefault(r["ip"], []).append(r)

    return grouped
