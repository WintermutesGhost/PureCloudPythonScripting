import

def updateToken():
    newToken = input("Please enter a new OAUTH token:\n")
    try:
        setAccessToken(newToken)
        print("Authentication successful!")
    except PureCloudPlatformClientV2.rest.ApiException:
        print("Authentication failed")
