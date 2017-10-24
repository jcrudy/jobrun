from datetime import datetime
import hashlib


def get_timestamp():
    return datetime.utcnow().strftime('%Y%m%d%H%M%S%f')

def ts(name):
    def _ts():
        timestamp = get_timestamp()
        return name % timestamp
    return _ts

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def none_to_empty_dict(arg):
    if arg is None:
        return {}
    else:
        return arg