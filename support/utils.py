'''
This module contains various utilitarian functions used by other modules.
'''

# ***************************************
# Imports
# ***************************************
import logging
import sys

# *****************************************
# Local variables
# *****************************************
_utilsLogger = logging.getLogger("monitoringProxy.main.utils")

# ***********************************************
# Functions
# ***********************************************
def exitFunc():
    '''
    exit process
    '''
    sys.exit(0)
