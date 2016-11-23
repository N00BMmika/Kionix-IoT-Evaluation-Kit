# 
# Copyright 2016 Kionix Inc.
#
"""Socket module for Nordic BLE usage

    Uses port forwarding to connect Android device socket

"""
import time, subprocess, sys

from socket_connection import SocketClient, SocketServer
from util_lib import logger

# CONSTANTS
DEVICE_SOCKET_PORT = 8123
LOCAL_SOCKET_PORT = 8100

ADB_PATH = 'adb.exe'
USE_PORT_FORWARD = True

class SocketSender(SocketClient):
    def __init__(self):
        SocketClient.__init__(self)
        self.__testAppSocketThread = None

    def _createSocketServer(self):
        """Create socket server for testing purposes."""
        socketServer = SocketServer()
        socketServer.startServer(LOCAL_SOCKET_PORT)

    def _prepareSocketConnection(self):
        """Create port forward to test app socket port. This is used for verification."""
        try:
            subprocess.call('%s forward --remove-all' % ADB_PATH)
        except WindowsError:
            logger.critical('ADB.EXE not found from PATH. Please install adb.exe / check PATH definitions.')
            sys.exit(1)

        if USE_PORT_FORWARD:
            subprocess.call('%s forward tcp:%s tcp:%s' % (ADB_PATH, str(LOCAL_SOCKET_PORT), str(DEVICE_SOCKET_PORT)))

        if self.connectToSocketServer(port=LOCAL_SOCKET_PORT):
            pass
        else:
            print 'Unable to connect to socket!'

    def closeSocketConnection(self):
        """Close socket connection."""
        if self.isOpen():
            self.disconnect()
            print 'socket connection closed'

            for i in range(10):
                if self.__testAppSocketThread:
                    if self.__testAppSocketThread.isAlive():
                        time.sleep(0.5)
                    else:
                        self.__testAppSocketThread = None
                else:
                    break

            # remove port forwarding
            subprocess.call('%s forward --remove-all' % ADB_PATH)
