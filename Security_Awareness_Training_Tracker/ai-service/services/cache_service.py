import redis
import hashlib
import json

# -------- REDIS CONNECTION (SAFE) --------
try:
    r = redis.Redis(
        host='localhost',
        port=6379,
        db=0,
        decode_responses=True  # returns string instead of bytes
    )
    r.ping()  # test connection
except Exception as e:
    print("Redis not available:", str(e))
    r = None

# -------- CONFIG --------
TTL = 900  # 15 minutes


# -------- KEY GENERATION --------
def generate_key(text):
    return hashlib.sha256(text.encode()).hexdigest()


# -------- GET CACHE --------
def get_cache(key):
    if not r:
        return None
    try:
        data = r.get(key)
        if data:
            return json.loads(data)
    except Exception as e:
        print("Cache read error:", str(e))
    return None


# -------- SET CACHE --------
def set_cache(key, value):
    if not r:
        return
    try:
        r.setex(key, TTL, json.dumps(value))
    except Exception as e:
        print("Cache write error:", str(e))