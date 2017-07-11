import PureCloudPlatformClientV2

# Local reference for telephony API
teleApi = PureCloudPlatformClientV2.apis.TelephonyProvidersEdgeApi()


def createWebRtc(phoneUser):
    """
    Generate a basic WebRTC phone for a given userId
    
    :param userId: PureCloud User object to associate WebRTC phone with
    :returns: PureCloud telephone object for newly created WebRTC
    """
    name = phoneUser.name
    lineName = name.lower().replace(' ','') + "_webrtc"
    requestBody = {'name':name, # TODO: Use correct objects instead of dict
                   'site':{'name':'Calgary'},
                   'base':{'name':'WebRTC'}, #TODO: Remove hard-coded params
                   'web_rtc_user':{'id':phoneUser.id},
                   'lines':{'name':lineName}
                   }
    response = teleApi.post_telephony_providers_edges_phones(requestBody)
    return response
