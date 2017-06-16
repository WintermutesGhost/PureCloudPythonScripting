import PureCloudPlatformClientV2
#from pctoolkit.core import buildSimpleAQF,TODAY,YESTERDAY 

convApi = PureCloudPlatformClientV2.apis.ConversationsApi()

def initiateCallFromMe(phoneNumber):
    callBody = {'phoneNumber' : phoneNumber}
    response = convApi.post_conversations_calls(callBody)
    return response

def terminateCall(interactionId):
    activeConv = convApi.get_conversation(interactionId)
    activeConv.state = 'disconnected'
    closedConv = convApi.patch_conversations_call(interactionId,activeConv)
    return closedConv
    

def initiateCallFromToken(phoneNumber,token):
    currentToken = PureCloudPlatformClientV2.configuration.access_token
    setAccessToken(token)
    initiateCallFromMe(phoneNumber)
    setAccessToken = currentToken

