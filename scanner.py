import subprocess, uuid, os
from config import SCAN_STORAGE_DIR
from utils import ensure_storage

def run_scan(url, deep=False, scan_type=None):
    scan_id = str(uuid.uuid4())[:8]
    output = f"[Scan ID: {scan_id}]\nURL: {url}\n\n"
    types = scan_type.split(',') if scan_type else ['ssl', 'headers']

    if 'ssl' in types:
        domain = url.split('//')[1].split('/')[0]
        result = subprocess.getoutput(f"echo | openssl s_client -connect {domain}:443 -servername {domain} 2>/dev/null | openssl x509 -noout -dates")
        output += f"🔐 SSL/TLS:\n{result}\n\n"

    if 'headers' in types:
        import requests
        try:
            res = requests.get(url, timeout=10)
            output += "🔐 Response Headers:\n"
            for h,v in res.headers.items():
                output += f"{h}: {v}\n"
        except Exception as e:
            output += f"Error fetching headers: {e}\n\n"

    ensure_storage()
    path = os.path.join(SCAN_STORAGE_DIR, f"{scan_id}.txt")
    with open(path, 'w') as f:
        f.write(output)
    return scan_id, path
      
