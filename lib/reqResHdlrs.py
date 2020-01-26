'''
This module contains various handler functions used by other modules.
'''

# ***************************************
# Imports
# ***************************************
import logging
from urllib.parse import urlparse

# *****************************************
# Local variables
# *****************************************
_reqResHdlrsLogger = logging.getLogger("monitoringProxy.main.reqResHdlrs")

# ***********************************************
# Functions
# ***********************************************
def reqHdlr(buffer):
    '''
    request handling process
    '''
    newBuffer = buffer.split(" ")[1]    
    o = urlparse(newBuffer[1])
    host = o.netloc
    port = o.port
    
    if host == "":
        host = o.path.split(":")[0]
        port = o.path.split(":")[1]
    elif host != "" and port == None:
        port = 80
    
#     if port == None:
#         port = 80
        
    return (buffer, host, port)


def resHdlr(buffer):
    '''
    response handling process
    '''
    return buffer

def _parse(buffer):
    newBuffer = buffer.split(" ")
    method = newBuffer[0].replace("b'", "")
    host, port = _parseURL(newBuffer[1])
    
    print(method + " => " + host + ":" + str(port))

def _parseURL(url):
    host = ""
    port = -1
    
    hostIndex = url.find("://")
    
    if hostIndex != 1:
        host = url[(hostIndex + 3):].split("/")[0]
    
    
    
    return (host, port)