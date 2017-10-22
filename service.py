# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 22:28:29 2016
@author: zhanghc
"""
#引入模块
import socket
import threading
import time
#创建socket
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#监听端口
s.bind(('127.0.0.1',9999))
s.listen(5)
print 'Waiting for connection...'
def talk(text):
    import jieba,os
    import os
    from bosonnlp import BosonNLP
    nlp = BosonNLP(os.environ['nPom9h4a.18434.tEA4SsUlkG8g'])
    print nlp.sentiment(' ')


def tcplink(sock,addr):
    print 'Accept new connection from %s:%s...' % addr
    while True:
        data=sock.recv(1024)
        time.sleep(1)
        if data=='exit' or not data:
            break
        talk(data)
    sock.close()
    print 'Connection from %s:%s closed.'%addr


while True:
    # 接受一个新连接
    sock, addr = s.accept()

    # 创建新线程来处理TCP连接
    t = threading.Thread(target=tcplink(sock, addr))

