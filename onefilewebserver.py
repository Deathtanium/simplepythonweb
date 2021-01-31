#!/usr/bin/env python3

import datetime
import sys
import socket
from threading import Thread

HOST = '192.168.0.122'
PORT = 80

serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serverSock.bind((HOST,PORT))

serverSock.listen(1)

def secretary():        #The secretary will serve you the proper resource :3
    while True:
        clientSock, clientAddr = serverSock.accept()
        clientAddr=clientAddr[0]    #actual addr is first element of a tuple
        
        request = clientSock.recv(1024).decode()
        print(request)
        
        #resource will contain the requested htdoc
        resource = request.split()
        resource = resource[1]
        if resource[0] == '/':
            resource = resource.replace('/','',1)
        
        if resource == '':
            resource = 'index.html'
        
        resource = 'www/'+resource
        
        #crafting response
        
        respCode = '200 OK'
        
        try:
            body = open(resource,'r')
        except FileNotFoundError:
            body = open('www/404.html','r')
            respCode = '404 Not Found'
        except IsADirectoryError:
            body = open('www/403.html','r')
            respCode = '403 Forbidden'
        
        response = f'HTTP/1.1 {respCode}\n\n{body.read()}'
        clientSock.send(response.encode())
        clientSock.close()
try:
    secretary()
except KeyboardInterrupt:
    print("Killed by keyboard")
