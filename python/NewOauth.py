import PureCloudUtils
import requests_oauthlib

ROLECOMM = '61cb8bf4-9778-41bf-a925-24d5181e1921'
ROLEEMP = 'c9a0f78e-9929-44a5-a3d2-735654885b65'

CLIENTID = r'd7656b6a-e543-4f1e-bf0c-c1f9a9ea9e8d'
CLIENTSECRET = r'IxhQfCvIMcEqNuEYbyonX_TxVTqaBaPlo1cId6lgJDA'
REDIRECTURI = 'https://www.getpostman.com/oauth2/callback'
AUTHURI = 'https://login.mypurecloud.com/oauth/authorize'

def getOauthToken():
    oauth = requests_oauthlib.OAuth2Session(CLIENTID, redirect_uri=REDIRECTURI)
    authUrl, state = oauth.authorization_url(AUTHURI)
