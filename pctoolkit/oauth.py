import socket
import re
import requests
import webbrowser
import time
import os
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

def listenForGetRequest(listenSock): # TODO: implement timeout,timeout=5):
    clientConnection,clientAddress = listenSock.accept()
    request = clientConnection.recv(1024)
    if clientConnection is None:
        return None
    getPathRegex = re.search(r'GET (\/.*) HTTP', str(request))
    logging.info('Request: %s',getPathRegex.group(0))
    if getPathRegex is None:
        raise ValueError("Request received is not a GET ")
    path = getPathRegex.group(1)
    return clientConnection,path

def parseGetRequest(path):
    STATUS200 = 'HTTP/1.1 200 OK'
    STATUS400 = 'HTTP/1.1 404 NOT FOUND'
    packagePath = os.path.dirname(os.path.abspath(__file__))
    responsePageName = 'oauthRedirect.html'
    responsePagePath = os.path.join(packagePath,responsePageName)
    response = {}
    if path == '/':
        with open(responsePagePath,'r') as responsePage:
            response['status'] = STATUS200
            response['body'] = responsePage.read()
    elif path.startswith('/token/'):
        response['token'] = path[7:]
        response['status'] = STATUS200
        response['body'] = ''
    else:
        response['status'] = STATUS400
        response['body'] = '404: Not found'
    return response

def sendResponse(clientConnection,response):
    httpResponse = response['status'] + '\n\n' + response['body']
    logging.info('Response: %s', response['status'])
    clientConnection.sendall(httpResponse.encode('utf-8'))
    clientConnection.close()


def requestToken():
    HOST = ''
    PORT = 8080
    TIMEOUT = 120
    LOCALHOST = 'http://localhost'
    listenSock = openListeningSocket(HOST, PORT)
    logging.info('Serving HTTP on port %s.',PORT)
    webbrowser.open(LOCALHOST+':'+str(PORT))
    logging.info('Browser opened to: %s', LOCALHOST+':'+str(PORT))
    startTime = time.time()
    while (time.time()-startTime) < TIMEOUT:
        clientConnection,requestPath = listenForGetRequest(listenSock)
        response = parseGetRequest(requestPath)
        sendResponse(clientConnection, response)
        if 'token' in response:
            logging.info("Token received: %s",response['token'])
            listenSock.close()
            return response['token']
    listenSock.close()
    logging.warning("No token received before timeout")
    
            
        
    
    