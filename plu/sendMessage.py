#coding=utf-8

def sendMessage(message,mac_id):
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8081))
    from plu import word2
    message=word2.wordstotwo(message+'?/!'+mac_id)
    sock.send(message)
    print sock.recv(1024)
    sock.close()