import PureCloudPlatformClientV2

# Local reference for telephony API
teleApi = PureCloudPlatformClientV2.apis.TelephonyProvidersEdgeApi()


def createWebRtc(user,siteName,baseName):
    """
    Generate a basic WebRTC phone for a given userId
    
    :param user: PureCloud User object to associate WebRTC phone with
    :param siteName: name of site to associate sith
    :param baseName: name of base configuration to build from
    :returns: PureCloud telephone object for newly created WebRTC
    """
    name = user.name
    lineName = name.lower().replace(' ','') + "_webrtc"
    requestBody = {'name':name, # TODO: Use PureCloud objects instead of dict
                   'site':{'name':siteName},
                   'base':{'name':baseName},
                   'web_rtc_user':{'id':user.id},
                   'lines':{'name':lineName}
                   }
    response = teleApi.post_telephony_providers_edges_phones(requestBody)
    return response
