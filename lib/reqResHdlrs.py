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
    o = urlparse(buffer.split(" ")[1])
    host = o.netloc
    port = o.port
    
    if host == "":
        host = o.path.split(":")[0]
        port = o.path.split(":")[1]
    elif host != "" and port == None:
        port = 80
        
    return (buffer, host, port)


def resHdlr(buffer):
    '''
    response handling process
    '''
    return buffer
