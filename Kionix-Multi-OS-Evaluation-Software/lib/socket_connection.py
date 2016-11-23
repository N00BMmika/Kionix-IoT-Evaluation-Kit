# 
# Copyright 2016 Kionix Inc.
#
"""Socket connection module.
    
    Generic socket level connection. Implementation made both for client 
    and server side.

"""

import socket, sys
from struct import unpack
DEFAULT_PORT = 31300


def getAvailableSocketPort():
    """Returns available socket port."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        # bind to port 0 --> system will give an available socket port
        sock.bind(('', 0))
        ipaddr, port = sock.getsockname()
        sock.close()
    except socket.error, err:
        # in error situation, 0 is returned
        print 'Socket error in getting available socket port: %s' % str(err)
        port = 0

    return port
    
def isSocketPortAvailable(port):
    """Checks if given port is available or not.
    
        Parameters

        port        port number (integer 1-65535)
        
        Returns True if port is available, otherwise False.
    """
    assert isinstance(port, int), 'Valid port parameter not given!'

    portAvailable = False

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)        
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1) # this was needed for Windows Vista
        # try binding to given port, if it succeeds port is available
        sock.bind(('', port))
        sock.close()
        portAvailable = True
    except socket.error, err:
        # socket is either in use or other error occurred
        print 'Socket error in checking port availability: %s' % str(err)

    return portAvailable

class SocketTimeoutException(Exception):
    """Exception class for socket timeout exceptions."""
    pass

class SocketErrorException(Exception):
    """Exception class for socket error exceptions."""
    pass

class SocketNonBlockingException(Exception):
    """Exception class for non blocking socket when no data is available."""
    pass


class SocketConnection(object):
    """Base class for socket connection.

        Includes methods for reading and writing to/from tcp/ip socket.
    """
    MESSAGE_TERMINATOR = '\n'
    MESSAGE_TERMINATOR_REPLACEMENT = '?#-'
    MAX_MESSAGE_LENGTH = 16384 #8192 #4096 # 2048

    def __init__(self):
        self.conn = None      # socket connection
        self.connFile = None  # file object made from connection
        self._sock = None     # socket object

    def sendMessage(self, message):
        """Sends string trough socket, adds LF to end """
        assert self.isOpen(), 'Connection was not open!'

        # if MESSAGE_TERMINATOR character is used inside the message,
        # replace it with MESSAGE_TERMINATOR_REPLACEMENT
        #message = message.replace(self.MESSAGE_TERMINATOR,
        #                          self.MESSAGE_TERMINATOR_REPLACEMENT)

        # cut message if it is too long
        # this should be OK if we know that end part of message is always
        # freeform text
        # MESSAGE_TERMINATOR length is 1
        if len(message) >= self.MAX_MESSAGE_LENGTH - 1:
            message = message[:self.MAX_MESSAGE_LENGTH - 4] + '...'

        # FIXME: how to check that all data is sent??
        try:
            bytesSent = self.connFile.write(message )#+ self.MESSAGE_TERMINATOR)        
            self.connFile.flush()
        except socket.error:
            try:
                self.disconnect()
            except Exception, e:
                print 'Problems with closing socket',e
            raise SocketErrorException

    def recv_msg(self, sock):
        # Read message length and unpack it into an integer
        raw_msglen = self.recvall(sock, 1)      
        #print 'raw_msglen: ', raw_msglen
        
        if not raw_msglen:
            return None
        msglen = unpack('<b', raw_msglen)[0]
        msglen = msglen - 1
        #print 'messageLen \r\n', msglen
        # Read the message data
        return self.recvall(sock, msglen)

    def recvall(self, sock, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = ''
        while len(data) < n:
            packet = sock.recv(n - len(data))
            
            if not packet:
                return None
            data += packet
            
        return data

    def receiveMessage(self, timeout = None, msg_length=19):
        """Reads line from socket, removes LF from the end.
        
            Parameters
                
                timeout (int in seconds) default = None
                                         (None uses timeout set in connectToSocketServer)
        """
        #print 'Enter receive message'
        assert self.isOpen(), 'Connection was not open!'
        
        if timeout is not None:
            self.conn.settimeout(timeout)
        try:
            #BUFFER_SIZE = 1024
            #socketMessage = ''
            #while 1:
            data = self.recv_msg(self.conn)
             #   msg = self.conn.recv(BUFFER_SIZE)
             #   msgLen = unpack('<b', msg[0])[0]
             #   print 'msgLen \r\n', msgLen
             #   socketMessage += msg
                
             #   if (len(socketMessage) - 1) == msgLen:
             #       print 'jes \r\n', len(socketMessage) - 1
             #       break
                #print 'nou \r\n',len(socketMessage), len(msg)
            return data
        except socket.timeout:
            raise SocketTimeoutException
        except socket.error:
            if timeout is not 0:
                raise SocketErrorException
            else:
                raise SocketNonBlockingException    
    def disconnect(self):
        """Close connFile and conn, which disconnects the socket."""
        # close socket if it's open
        if self.isOpen():
            self.connFile.close()
            self.conn.close()
            self.conn = None
            self.connFile = None

    def isOpen(self):
        """Returns if the socket is open or not."""
        return self.connFile is not None


class SocketClient(SocketConnection):
    """Class for socket client.

        Includes methods for connecting to socket server.
    """
    def connectToSocketServer(self, host = 'localhost',
                              port = DEFAULT_PORT, timeout = 0.2):
        
        """ Open connection to socket server with timeout.

        Parameters

            host    (Str) default 'localhost'

            port    (int) default DEFAULT_PORT
            
            timeout (int in seconds) default = 0.2

        Returns True and sets self.conn and self.connFile when connection is established.
        Otherwise (timeout) returns False
        """
        assert self.conn == None
        assert self.connFile == None

        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.settimeout(timeout)
        self.conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)

        try:
            self.conn.connect((host, port))
        except socket.timeout:
            self.conn.close()
            self.conn = None
            return False
        except socket.error, err:
            self.conn.close()
            self.conn = None
            return False
        
        self.connFile = self.conn.makefile()
        return True


class SocketServer(SocketConnection):
    """Class for socket server.

        Includes methods for creating socket server.
    """
    def startServer(self, port = DEFAULT_PORT):
        """Start the socket server to wanted host and port.

        port            -- Port number (default=DEFAULT_PORT)

        Blocks until client connects to server and 
        returns True when client has connected to server.
        """
        serverSock = None

        serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        addr = ('localhost', port)

        try:
            serverSock.bind(addr)
            serverSock.listen(1)
        except socket.error, err:
            print 'Error in socket binding: %s' % str(err)
            serverSock.close()
            serverSock = None
            raise err

        if serverSock is None:
            print 'Could not open socket connection!'
            # FIXME: do not use sys.exit()
            #        own exception class??
            sys.exit(1)

        conn, addr = serverSock.accept()
        print 'Socket connection from: ', addr
        
        # store socket object to self
        # NOTE: This is important! Otherwise socket open/close status can't
        #       be seen from other processes.
        self._sock = serverSock

        self.conn = conn
        self.connFile = conn.makefile()

        return True
