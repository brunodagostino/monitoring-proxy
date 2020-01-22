'''
This module contains the proxy server class used by other modules.
'''

# ***************************************
# Imports
# ***************************************
import socket


class ProxyServer:
    addrFamily = socket.AF_INET
    sockType = socket.SOCK_STREAM
    reqQueueSize = 5
    allowReuseAddr = False

    def __init__(self, localHost, localPort, recvFirst, bindAndActivate=False):
        self.sock = socket.socket(self.addrFamily, self.sockType)
        self.localHost = localHost
        self.localPort = localPort
        self.recvFirst = recvFirst
        
        if bindAndActivate:
            try:
                self.serverBind()
                self.serverActivate()
            except:
                self.serverClose()
                raise
                
    def serverBind(self):
        if self.allowReuseAddr:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.sock.bind((self.localHost, self.localPort))
        
        self.serverAddr = self.sock.getsockname()
    
    def serverActivate(self):
        self.sock.listen(self.reqQueueSize)
    
    def serverClose(self):
        self.sock.close()
    
    def getReq(self):
        return self.sock.accept()
