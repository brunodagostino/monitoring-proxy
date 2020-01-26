'''
This module contains the proxy handler function used by other modules.
'''

# ***************************************
# Imports
# ***************************************
import logging
import socket

from lib.readBuffer import recvFrom
from lib.reqResHdlrs import reqHdlr, resHdlr

# *****************************************
# Local variables
# *****************************************
_proxyHdlrLogger = logging.getLogger("monitoringProxy.main.proxyHdlr")

# ***********************************************
# Functions
# ***********************************************
def proxyHdlr(clientSock):
    '''
    proxy handler process
    '''        
    global _proxyHdlrLogger
    
    while True:
        localBuffer = recvFrom(clientSock)
                        
        if len(localBuffer):
            localBuffer, remoteHost, remotePort = reqHdlr(localBuffer)
            
            remoteSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remoteSocket.connect((remoteHost, remotePort))
            remoteSocket.send(localBuffer)
        
        remoteBuffer = recvFrom(remoteSocket)
        
        remoteSocket.close()
        
        if len(remoteBuffer):
            remoteBuffer = resHdlr(remoteBuffer)
            
            clientSock.send(remoteBuffer)
#             _proxyHdlrLogger.log(logging.INFO, "[Proxy handler] " + localBuffer)
        
        if not len(localBuffer) or not len(remoteBuffer):
            clientSock.close()
#             remoteSocket.close()
            
            break