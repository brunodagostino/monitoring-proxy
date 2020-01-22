#! python3

'''
Main method along with argument parsing functions
'''

# ************************************************************
# Imports
# ************************************************************
import sys
import argparse
import logging
import threading

from support.utils import exitFunc
from lib.proxyServer import ProxyServer
from lib.proxyHdlr import proxyHdlr


def displayHelp(parserHelp):
    '''
    displays help prompt
    '''
    parserHelp.print_help()


def parseCommandline(parser):
    '''
    parses arguments given to commandline
    '''
    parser.add_argument("-lh", "--localhost", type=str, default="127.0.0.1", help="localhost")
    parser.add_argument("-lp", "--localport", type=int, default=9000, help="localport")
    parser.add_argument("-rf", "--receivefirst", default=False, action="store_true", help="receive first")
    
    if len(sys.argv) >= 5:
        displayHelp(parser)
        exitFunc()
    
    return parser.parse_args()


def closeUp():
    for thread in proxyThreads:
        thread.join()
        
    proxyServer.serverClose()
    sys.exit()


if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    args = parseCommandline(parser)

    # set verbose output on or off
    mainLogger = logging.getLogger("monitoringProxy.main")
    fileHdlr = logging.FileHandler("log.txt")
    fileHdlr.setLevel(logging.INFO)
    mainLogger.addHandler(fileHdlr)
    mainLogger.setLevel(logging.INFO)
                
    proxyServer = ProxyServer(args.localhost, args.localport, args.receivefirst)
    proxyServer.serverBind()
    proxyServer.serverActivate()
    
    proxyThreads = []
    
    try:
        while True:
            clientSock, addr = proxyServer.getReq()
        
            mainLogger.log(logging.INFO, "Received incoming connection from " + addr[0] + ":" + str(addr[1]))
            
            proxyThreads.append(threading.Thread(target=proxyHdlr, args=(clientSock,)))
            proxyThreads[-1].start()
    except KeyboardInterrupt as e:
        print("[MonitoringProxy] occured while handling KeyboardInterrupt exception: \n" + str(e))
    
    closeUp()
