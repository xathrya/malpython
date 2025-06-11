# MalPython
#
# Compile string of python code and execute it

import platform 

# code snippet for executing (evaluate) python code

def payload():
    name = platform.system()
    if name.startswith("Linux"):
        code="print('MalPython code for Linux')"
    elif name.startswith("Windows"):
        code="print('MalPython code for Windows')"
    elif name.startswith("Darwin"):
        code="print('MalPython code for macOS')"
    else:
        code="pass"
    
    exec(compile(code,"<string>","exec"))

payload()