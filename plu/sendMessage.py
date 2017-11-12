#coding=utf-8
def sendMessage(message,mac_id):
    from pub import get_config
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', int(get_config.get_porttext())))
    from plu import word2
    message=word2.wordstotwo(message+'?/!'+mac_id)
    print sock.send(message)
    recv= sock.recv(1024)
    sock.close()
    return recv
