import PureCloudPlatformClientV2
from pctoolkit.core import buildSimpleAQF,TODAY,YESTERDAY 

convApi = PureCloudPlatformClientV2.apis.ConversationsApi()

def initiateCallFromMe(phoneNumber):
    callBody = {'phoneNumber' : phoneNumber}
    response = convApi.post_conversations_calls(callBody)
    return response

def initiateCallFromToken(phoneNumber,token):
    currentToken = PureCloudPlatformClientV2.configuration.access_token
    setAccessToken(token)
    initiateCallFromMe(phoneNumber)
    setAccessToken = currentToken

