import platform 

# define function which contain payload
def payload():
    if platform.system().startswith("Linux"):
        code="print('MalPython code for Linux')"
    elif platform.system().startswith("Windows"):
        code="print('MalPython code for Windows')"
    elif platform.system().startswith("Darwin"):
        code="print('MalPython code for macOS')"
    else:
        code="pass"
    
    eval(compile(code, "<string>", "exec"))

# execute the payload immediately
payload()