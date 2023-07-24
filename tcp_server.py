#******************************************************************************
# File Name:   tcp_server.py
#
# Description: A simple "tcp server" for demonstrating TCP usage.
# The server sends LED ON/OFF commands to the connected TCP client
# and receives acknowledgement from the client.
#
#
#******************************************************************************
# $ Copyright 2021-2023 Cypress Semiconductor $
#******************************************************************************

#!/usr/bin/python

import socket
import optparse
import time
import sys
import threading

host = socket.gethostbyname(socket.gethostname())  # IP address of the TCP server
port = 50007                                       # Arbitrary non-privileged port
RECV_BUFF_SIZE = 4096                              # Receive buffer size
DEFAULT_KEEP_ALIVE = 1                             # TCP Keep Alive: 1 - Enable, 0 - Disable

print("==========================")
print("TCP Server")
print("==========================")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# set TCP Keepalive parameters
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 10)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 1)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 2)
s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, DEFAULT_KEEP_ALIVE)

# variable to identify if there is an active client connection
is_client_connected = False

class KeyboardThread(threading.Thread):

    def __init__(self, input_cbk = None, name='keyboard-input-thread'):
        self.input_cbk = input_cbk
        super(KeyboardThread, self).__init__(name=name)
        self.start()

    def run(self):
        while True:
            self.input_cbk(input()) #waits to get input + Return

def read_user_data(inp):
    #evaluate the keyboard input
    if(is_client_connected == True):
        if(inp == ""):
            print("No option entered!")
            print("Enter your option: '1' to turn ON LED, 0 to turn"\
                            " OFF LED and Press the 'Enter' key: ")
        else:
            conn.send(inp.encode())
    else:
        print("No active client connection. Command not send")

#start the Keyboard thread
kthread = KeyboardThread(read_user_data)

# Bind the socket to host IP address and port
try:
    s.bind((host, port))
    s.listen(1)
except socket.error as msg:
    print("ERROR: ", msg)
    s.close()
    s = None

if s is None:
    sys.exit(1)

while True:    
    try:
        is_client_connected = False;
        print("Listening on: IPv4 Address: %s Port: %d"%(host, port))
        conn, addr = s.accept()
        is_client_connected = True
           
    except KeyboardInterrupt:
        print("Closing Connection")
        s.close()
        s = None
        sys.exit(1)

    print('Incoming connection accepted: ', addr)

    while True:
        try:
            print("Enter your option: '1' to turn ON LED, 0 to turn"\
                        " OFF LED and Press the 'Enter' key: ")
            
            data = conn.recv(RECV_BUFF_SIZE)
            if not data: break
            print("Acknowledgement from TCP Client:", data.decode('utf-8'))
            print("")
            
        except socket.error:
            print("Timeout Error! TCP Client connection closed")
            break
            
        except KeyboardInterrupt:
            print("Closing Connection")
            s.close()
            s = None
            sys.exit(1)    

# [] END OF FILE
