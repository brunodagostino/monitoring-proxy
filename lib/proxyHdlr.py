'''
This module contains the proxy handler function used by other modules.
'''

# ***************************************
# Imports
# ***************************************
import socket

from lib.readBuffer import recvFrom
from lib.reqResHdlrs import reqHdlr, resHdlr


# ***********************************************
# Functions
# ***********************************************
def proxyHdlr(clientSock):
    '''
    proxy handler process
    '''            
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
        
        if not len(localBuffer) or not len(remoteBuffer):
            clientSock.close()
            
            break
