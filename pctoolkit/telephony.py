import PureCloudPlatformClientV2

teleApi = PureCloudPlatformClientV2.apis.TelephonyProvidersEdgeApi()


def createWebRtc(userId):
    name = getUser(userId).name
    lineName = name.lower().replace(' ','') + "_webrtc"
    requestBody = {'name':name,
                   'site':{'name':'Calgary'},
                   'base':{'name':'WebRTC'},
                   'web_rtc_user':{'id':userId},
                   'lines':{'name':lineName}
                   }
    response = teleApi.post_telephony_providers_edges_phones(requestBody)
    return response
