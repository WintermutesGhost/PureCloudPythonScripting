import socket
import re
import requests
import webbrowser
import time
import logging #TODO: Use Elsewhere?

import PureCloudPlatformClientV2

logging.basicConfig(level=logging.INFO) #TODO: Non-basic logging?

def setAccessToken(newToken):
    PureCloudPlatformClientV2.configuration.access_token = newToken

def openListeningSocket(host,port):
    listenSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listenSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listenSock.bind((host,port))
    listenSock.listen(1)
    return listenSock

def listenForGetRequest(listenSock) # TODO: implement timeout,timeout=5):
    clientConnection,clientAddress = listenSock.accept()
    request = clientConnection.recv(1024)
    if clientConnection is None:
        return None
    getPathRegex = re.search(r'GET (\/.*) HTTP', request)
    logging.info('Request received: %s',getPathRegex.group(0))
    if getPathRegex is None:
        raise ValueError("Request received is not a GET ")
    path = getPathRegex.group(1)
    return path

def parseGetRequest(path):
    pass

def sendResponse():
    pass

def requestAuthentication():
    HOST = ''
    PORT = 8080
    TIMEOUT = 120
    listenSock = openListeningSocket(HOST, PORT)
    logging.info('Serving HTTP on port %s.',PORT)
    startTime = time.time()
    while (time.time()-startTime) < TIMEOUT:
        requestPath = listenForGetRequest(listenSock)
        
    
    