'''
This module contains the proxy handler function used by other modules.
'''

# ***************************************
# Imports
# ***************************************
import socket
import logging

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
    
    remoteSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    flag = False
    
    while True:
        localBuffer = recvFrom(clientSock)
#     localBuffer = clientSock.recv(4096)
                        
        if len(localBuffer):
            _proxyHdlrLogger.log(logging.INFO, "[ProxyHandler] " + str(localBuffer))
            localBuffer, remoteHost, remotePort = reqHdlr(localBuffer)
            _proxyHdlrLogger.log(logging.INFO, "[ProxyHandler] " + str(localBuffer) + " | " + remoteHost + ":" + str(remotePort))
                       
#             remoteSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if flag == False:
                flag = True
                remoteSock.connect((remoteHost, remotePort))
                remoteSock.send(localBuffer)
    
        remoteBuffer = recvFrom(remoteSock)
#         remoteBuffer = remoteSocket.recv(4096)
                
        if len(remoteBuffer):
            remoteBuffer = resHdlr(remoteBuffer)
            
            clientSock.send(remoteBuffer)
        
        if not len(localBuffer) or not len(remoteBuffer):
            clientSock.close()
            remoteSock.close()
            flag = False
            
            break