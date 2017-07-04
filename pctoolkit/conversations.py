import PureCloudPlatformClientV2
import time # Only used to avoid hitting API limits
#from pctoolkit.core import buildSimpleAQF,TODAY,YESTERDAY 

convApi = PureCloudPlatformClientV2.apis.ConversationsApi()

def initiateCallFromMe(phoneNumber):
    callBody = {'phoneNumber' : phoneNumber}
    response = convApi.post_conversations_calls(callBody)
    return response

def terminateCall(interactionId):
    #activeConv = convApi.get_conversation(interactionId)
    #activeConv.state = 'disconnected'
    #convTemplate = PureCloudPlatformClientV2.Conversation
    convTemplate = {'state' : 'disconnected'}
    closedConv = convApi.patch_conversations_call(interactionId,convTemplate)
    return closedConv

def getConversationList(conversationIds):
    convList = []
    for convId in conversationIds:
        convList += convApi.get_conversation(convId)
        # Sleep to avoid hitting API rate limits, pending a better solution
        time.sleep(0.4) 
        # TODO: Exception handling for graceful conversation not founds
    return convList