# MalPython
# 
# Monkeypatch the module, hook the function and add additional behavior
# Payload should be executed before the target module

import os 

__o_system = os.system

def malicious_system(cmd):
    print(f"[!] intercepted command: {cmd}")
    return __o_system(cmd)

os.sytem = malicious_system

# combine with sys.meta_path or sys.path_hooks to modify import module