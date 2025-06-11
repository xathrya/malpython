# MalPython
#
# Execute payload when python exists

import atexit 

def payload():
    print("MalPython - Execution at Exit")

atexit.register(payload))