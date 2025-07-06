import re, os
from config import SCAN_STORAGE_DIR
from datetime import datetime, timedelta
from collections import defaultdict

rate_limits = defaultdict(list)

def is_valid_url(url):
    return re.match(r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$', url)

def check_rate_limit(user_id):
    now = datetime.utcnow()
    rate_limits[user_id] = [ts for ts in rate_limits[user_id] if now - ts < timedelta(days=1)]
    if len(rate_limits[user_id]) >= RATE_LIMIT:
        return False
    rate_limits[user_id].append(now)
    return True

def ensure_storage():
    if not os.path.exists(SCAN_STORAGE_DIR):
        os.makedirs(SCAN_STORAGE_DIR)
  
