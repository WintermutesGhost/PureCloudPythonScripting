import time # Only used to avoid hitting API limits

import PureCloudPlatformClientV2

# Local reference for conversations API
convApi = PureCloudPlatformClientV2.apis.ConversationsApi()

def initiateCallFromMe(phoneNumber):
    """
    Initiates a call from the user currently authenticated
    
    Calls will not succeed unless the "Pleacing calls with another app?"
    option is first enabled in the PureCloud web interface
    
    :param phoneNumber: phone number to place a call to
    :returns: PureCloud conversation object for placed call
    """
    callBody = {'phoneNumber' : phoneNumber}
    response = convApi.post_conversations_calls(callBody)
    return response

def terminateCall(interactionId): #TODO: Rename to interaction, not just call
    """
    Disconnects all participants and ends an interaction
    
    :param interactionId: PureCloud interaction ID to disconnect
    :returns: updated PureCloud conversation object for placed call
    """
    convTemplate = {'state' : 'disconnected'}
    closedConv = convApi.patch_conversations_call(interactionId,convTemplate)
    return closedConv

def getConversationList(conversationIds): #TODO: renams
    """
    Returns PureCloud conversation objects for a list of conversation IDs
    
    Slow, as each request runs individually and requires 0.4 seconds to avoid
    rate limits.
    
    :param conversationIds: iterable list of conversation IDs to retrieve
    :returns: list of PureCloud conversation objects retrieved
    """
    convList = []
    for convId in conversationIds:
        convList.append(convApi.get_conversation(convId))
        # Sleep to avoid hitting API rate limits, pending a better solution
        time.sleep(0.4) 
        # TODO: Exception handling for graceful conversation not founds
    return convList