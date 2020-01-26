'''
This module contains the read buffer function used by other modules.
'''


# ***********************************************
# Functions
# ***********************************************
def recvFrom(conn):
    '''
    read buffer process
    '''
    buffer = b""
    
    conn.settimeout(2)
    
    try:
        while True:
            data = conn.recv(4096)
            
            if not data:
                break
            
            buffer += data
    except:
        pass
    
    return buffer
