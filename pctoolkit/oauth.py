import socket
import re
import webbrowser
import time
import os
import logging #TODO: Add logging functionality elsewhere in package

import PureCloudPlatformClientV2

from pctoolkit.users import usersApi

#TODO: Remove logging by default
#TODO: Move to specific logger instead of root logger
logging.basicConfig(level=logging.INFO) 

def setAccessToken(newToken):
    """
    Configure and validate a new access token
    
    Uses GET /api/v2/users/me to validate, so code grant tokens will not work
    
    :param newToken: new token value to use
    :raises ConnectionError: token validation failed
    """
    PureCloudPlatformClientV2.configuration.access_token = newToken
    try:
        usersApi.get_users_me()
    except PureCloudPlatformClientV2.rest.ApiException:
        raise ConnectionError("Cannot validate token")

def openListeningSocket(host,port):
    """
    Open a listening socket for handling HTTP requests
    
    :param host: local host extention to (http://localhost)
    :param port: local port to listen on
    :returns: socket object which is listening for connections
    """
    listenSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listenSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listenSock.bind((host,port))
    listenSock.listen(1)
    return listenSock

def listenForRequest(listenSock):
    """
    Check if a request is waiting on the socket and return the connection
    
    Accepts open requests and returns the ClientConnection object, as well as
    the path requested for retrieval.
    
    :param listenSock: socket object to listen on
    :returns: request body
    :returns: connection object with the requestor
    """
    clientConnection,clientAddress = listenSock.accept()
    request = clientConnection.recv(1024)
    if clientConnection is None:
        return None
    return request,clientConnection

def extractGetRequestPath(request):
    """
    Pull request path out of a HTTP GET request
    
    Non GET requests raise error
    
    :param request: HTTP request to get path for
    :raises Value Error: request received that is not a GET
    :returns: string of path request was seeking
    """
    getPathRegex = re.search(r'GET (\/.*) HTTP', str(request))
    logging.info('Request: %s',getPathRegex.group(0))
    if getPathRegex is None:
        raise ValueError("Request received is not a GET ") #TODO: Graceful handling?
    path = getPathRegex.group(1)
    return path

def parseGetRequest(request):
    """
    Parse incoming request and generate appropriate response for simple oauth
    
    If request is for path '/', serves oauthRedirect.html page. If request is
    for '/token/', serve nothing. Else, return 404.
    
    :param request: HTTP request body
    :returns: dict with response status, body and token (if applicable)
    """
    requestPath = extractGetRequestPath(request)
    STATUS200 = 'HTTP/1.1 200 OK'
    STATUS400 = 'HTTP/1.1 404 NOT FOUND'
    packagePath = os.path.dirname(os.path.abspath(__file__))
    responsePageName = 'oauthRedirect.html'
    responsePagePath = os.path.join(packagePath,responsePageName)
    response = {}
    if requestPath == '/':
        with open(responsePagePath,'r') as responsePage:
            response['status'] = STATUS200
            response['body'] = responsePage.read()
    elif requestPath.startswith('/token/'):
        response['token'] = requestPath[7:]
        response['status'] = STATUS200
        response['body'] = ''
    else:
        response['status'] = STATUS400
        response['body'] = '404: Not found'
    return response

def sendResponse(clientConnection,response):
    """
    Send response back to client connection
    
    Response should have 'status' and 'body'
    
    :param clientConnection: client connection object to send response to
    :param response: dict with ['status'] and ['body'] to send
    """
    httpResponse = response['status'] + '\n\n' + response['body']
    logging.info('Response: %s', response['status'])
    clientConnection.sendall(httpResponse.encode('utf-8'))
    clientConnection.close()

def requestAccessToken():
    """
    Run a full request to retrieve a new access token
    
    Opens a socket on localhost to serve HTTP, opens client browser pointed 
    at the localhost, serves a basic page which redirects to the PureCloud 
    auth page, receives the token and passes it back.
    
    :returns: new token retrieved 
    """
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
        request,clientConnection = listenForRequest(listenSock)
        response = parseGetRequest(request)
        sendResponse(clientConnection, response)
        if 'token' in response:
            logging.info("Token received: %s",response['token'])
            listenSock.close()
            return response['token']
    listenSock.close()
    logging.warning("No token received before timeout")