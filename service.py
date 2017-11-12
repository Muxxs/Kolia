#coding=utf-8
import socket
import sys
from thread import *
from pub import get_config
HOST = ''  # Symbolic name meaning all available interfaces
PORT = int(get_config.get_porttext() ) # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error, msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

# Start listening on socket
s.listen(10)
print 'Socket now listening'


# Function for handling connections. This will be used to create threads
def clientthread(conn):
    # Sending message to connected client
    # infinite loop so that function do not terminate and thread do not end.
    while True:
        # Receiving from client
        data = conn.recv(1024)
        from plu_for_service import word2
        mes=word2.twotowords(str(data))
        message=mes.split("?/!")[0]
        model=mes.split("?/!")[1]
        from plu_for_service import kolia_text
        ret= kolia_text.text(str(message).encode("utf-8"))
        print ret
        conn.send(ret)  # send only takes string
    # came out of loop
    conn.close()
# now keep talking with the client
while 1:
    # wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread, (conn,))
s.close()
