# # main.py

#####BAsic Scanning

# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import List, Union, Dict
# from scanner import scan_targets

# app = FastAPI()

# # CORS for frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class ScanRequest(BaseModel):
#     targets: List[str]
#     udp: bool = False
#     profile: str = "quick"
#     ports: Union[int, List[int]] = 1000
#     threads: int = 100
#     timeout: int = 2

# @app.post("/scan")
# async def scan(request: ScanRequest):
#     try:
#         print(f"⏳ Scan started with: {request.targets}")

#         results: Dict[str, List[dict]] = {}

#         # Scan each target separately
#         for target in request.targets:
#             scan_result = await scan_targets(
#                 ScanRequest(
#                     targets=[target],
#                     udp=request.udp,
#                     profile=request.profile,
#                     ports=request.ports,
#                     threads=request.threads,
#                     timeout=request.timeout,
#                 )
#             )
#             results[target] = scan_result

#         print("✅ Scan complete")
#         return {"status": "success", "results": results}

#     except Exception as e:
#         print("❌ Scan failed:", e)
#         raise HTTPException(status_code=500, detail=str(e))


####### multiple port scanning
# # backend/main.py
# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import List, Optional
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# origins = [
#     "http://localhost:5173",
#     "http://127.0.0.1:5173"
# ]

# # CORS for frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class ScanRequest(BaseModel):
#     targets: List[str]
#     profile: str = "quick"       # quick, full, custom
#     udp: bool = False
#     ports: Optional[List[int]] = None   # only used if custom

# @app.post("/scan")
# def scan_targets(request: ScanRequest):
#     results = {}

#     # define port ranges
#     if request.profile == "quick":
#         port_list = range(1, 101)
#     elif request.profile == "full":
#         port_list = range(1, 1001)
#     elif request.profile == "custom" and request.ports:
#         port_list = request.ports
#     else:
#         port_list = range(1, 101)

#     for target in request.targets:
#         # 🔍 Replace this mock with your actual scanning function
#         open_ports = []
#         for port in port_list:
#             # dummy rule: pretend port 22 and 80 are open
#             if port in [22, 80, 8080, 3306]:
#                 open_ports.append({
#                     "ip": "127.0.0.1" if target == "localhost" else target,
#                     "port": port,
#                     "protocol": "TCP",
#                     "service": "ssh" if port == 22 else "http" if port in [80, 8080] else "mysql",
#                     "banner": "N/A"
#                 })

#         results[target] = open_ports if open_ports else []
#     return results


#######fully functional with port status
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import socket
# import ipaddress

# app = FastAPI()

# # Allow frontend (Vite/React) to connect
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class ScanRequest(BaseModel):
#     targets: list[str]
#     profile: str = "quick"   # "quick" or "full"
#     udp: bool = False
#     verbose: bool = False


# # Profiles: which ports to scan
# PROFILES = {
#     "quick": [21, 22, 25, 53, 80, 110, 143, 443],
#     "full": list(range(1, 1025))
# }


# def get_service(port, protocol="TCP"):
#     try:
#         return socket.getservbyport(port, protocol.lower())
#     except:
#         return "unknown"


# def scan_target(ip, ports, udp=False, verbose=False):
#     scanned_ports = []

#     for port in ports:
#         port_info = {
#             "ip": ip,
#             "port": port,
#             "protocol": "UDP" if udp else "TCP",
#             "service": get_service(port, "udp" if udp else "tcp"),
#             "banner": None,
#             "status": "closed"
#         }

#         try:
#             if udp:
#                 s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#                 s.settimeout(1)
#                 s.sendto(b"", (ip, port))
#                 try:
#                     data, _ = s.recvfrom(1024)
#                     port_info["status"] = "open"
#                     port_info["banner"] = data.decode(errors="ignore")
#                 except socket.timeout:
#                     pass
#                 finally:
#                     s.close()
#             else:
#                 s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#                 s.settimeout(1)
#                 result = s.connect_ex((ip, port))
#                 if result == 0:
#                     port_info["status"] = "open"
#                     try:
#                         s.send(b"\r\n")
#                         banner = s.recv(1024).decode(errors="ignore").strip()
#                         if banner:
#                             port_info["banner"] = banner
#                     except:
#                         pass
#                 s.close()
#         except Exception as e:
#             port_info["status"] = f"error: {str(e)}"

#         scanned_ports.append(port_info)

#     # Return based on verbose
#     if verbose:
#         return scanned_ports
#     else:
#         return {
#             "open": [p for p in scanned_ports if p["status"] == "open"],
#             "closed": [p for p in scanned_ports if p["status"] == "closed"]
#         }


# @app.post("/scan")
# def scan(request: ScanRequest):
#     results = {}
#     ports = PROFILES.get(request.profile, PROFILES["quick"])

#     for target in request.targets:
#         try:
#             ip = str(ipaddress.ip_address(target)) if not target.replace(".", "").isdigit() else target
#         except:
#             try:
#                 ip = socket.gethostbyname(target)
#             except:
#                 results[target] = {"error": "Invalid host"}
#                 continue

#         results[target] = scan_target(ip, ports, udp=request.udp, verbose=request.verbose)

#     return results


# @app.get("/ping")
# def ping():
#     return {"message": "pong 🏓 from FastAPI!"}




# #####finalll
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import List, Union
# from scanner import scan_targets

# app = FastAPI()

# # Allow frontend React app to call backend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Input model for scan requests
# class ScanRequest(BaseModel):
#     targets: List[str]
#     udp: bool = False
#     profile: str = "quick"
#     ports: Union[int, List[int]] = 100
#     threads: int = 100
#     timeout: int = 2
#     verbose: bool = False   # 👈 NEW

# @app.get("/ping")
# async def ping():
#     return {"message": "pong 🏓 from FastAPI!"}

# @app.post("/scan")
# async def scan(request: ScanRequest):
#     try:
#         print(f"⏳ Scan started with data: {request}")

#         results = await scan_targets(request)

#         print("✅ Scan complete")
#         return {"status": "success", "results": results}

#     except Exception as e:
#         print("❌ Scan failed:", e)
#         raise HTTPException(status_code=500, detail=str(e))



from fastapi import FastAPI
from pydantic import BaseModel
import socket
import ipaddress
import asyncio
import string

app = FastAPI()

# --------------------------
# Profiles
# --------------------------
PROFILES = {
    "quick": [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3389],
    "full": list(range(1, 100)),
    "custom": []  # can be set dynamically
}

# --------------------------
# CORS (for frontend React)
# --------------------------
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust to ["http://localhost:5173"] if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------
# Request Model
# --------------------------
class ScanRequest(BaseModel):
    targets: list[str]
    profile: str = "quick"
    udp: bool = False
    verbose: bool = False

# --------------------------
# Banner sanitization
# --------------------------
def sanitize_banner(banner_bytes):
    """Convert banner bytes to readable ASCII, ignore non-printable chars"""
    try:
        text = banner_bytes.decode(errors="ignore")
        printable = "".join(ch for ch in text if ch in string.printable)
        return printable.strip() or None
    except Exception:
        return None

# --------------------------
# TCP Scan
# --------------------------
async def tcp_scan(ip: str, port: int) -> dict:
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(ip, port), timeout=1)
        banner = None
        try:
            writer.write(b"HELLO\r\n")
            await writer.drain()
            raw_banner = await asyncio.wait_for(reader.read(100), timeout=1)
            banner = sanitize_banner(raw_banner)
        except Exception:
            pass
        writer.close()
        await writer.wait_closed()
        return {
            "ip": ip,
            "port": port,
            "protocol": "TCP",
            "status": "open",
            "service": socket.getservbyport(port, "tcp") if port < 1024 else "unknown",
            "banner": banner
        }
    except Exception:
        return {"ip": ip, "port": port, "protocol": "TCP", "status": "closed"}

# --------------------------
# UDP Scan
# --------------------------
async def udp_scan(ip: str, port: int) -> dict:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)
        sock.sendto(b"HELLO", (ip, port))
        try:
            data, _ = sock.recvfrom(1024)
            banner = sanitize_banner(data)
            return {
                "ip": ip,
                "port": port,
                "protocol": "UDP",
                "status": "open",
                "service": socket.getservbyport(port, "udp") if port < 1024 else "unknown",
                "banner": banner
            }
        except socket.timeout:
            return {"ip": ip, "port": port, "protocol": "UDP", "status": "closed"}
    except Exception:
        return {"ip": ip, "port": port, "protocol": "UDP", "status": "closed"}

# --------------------------
# Scan single target
# --------------------------
async def scan_target(ip: str, port: int, udp: bool = False):
    return await (udp_scan(ip, port) if udp else tcp_scan(ip, port))

# --------------------------
# Expand CIDR / Targets
# --------------------------
def expand_targets(targets: list[str]):
    expanded = []
    for target in targets:
        try:
            if "/" in target:
                network = ipaddress.ip_network(target, strict=False)
                expanded.extend([str(ip) for ip in network.hosts()])
            else:
                expanded.append(target)
        except Exception:
            expanded.append(target)
    return expanded

# --------------------------
# API Endpoint
# --------------------------
@app.post("/scan")
async def scan(request: ScanRequest):
    targets = expand_targets(request.targets)
    profile = request.profile
    udp = request.udp
    verbose = request.verbose

    results = {}

    for ip in targets:
        ports_to_scan = PROFILES.get(profile, PROFILES["quick"])
        scan_results = []

        # Scan each port
        for port in ports_to_scan:
            res = await scan_target(ip, port, udp)
            if verbose:
                scan_results.append(res)
            elif res["status"] == "open":
                scan_results.append(res)

        # If nothing is open, return a friendly message
        if not scan_results:
            results[ip] = [{"ip": ip, "status": "no open ports found"}]
        else:
            results[ip] = scan_results

    return {"status": "success", "results": results}
