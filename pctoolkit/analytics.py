import PureCloudPlatformClientV2
from pctoolkit.core import buildSimpleAQF,TODAY,YESTERDAY 

anaApi = PureCloudPlatformClientV2.apis.AnalyticsApi()

#TODO: Make these timesone-aware


def buildPresenceQueryBody(interval,presenceFilters: list,routingFilters: list,userFilters: list, pageNumber = 1):
    body = PureCloudPlatformClientV2.UserDetailsQuery()
    body.interval = interval
    if presenceFilters:
        pf = {'systemPresence':o for o in presenceFilters}
        body.presence_filters = [buildSimpleAQF(pf, 'or')]
    if routingFilters:
        rf = {'routingStatus':o for o in routingFilters}
        body.routing_status_filters = [buildSimpleAQF(rf, 'or')]
    if userFilters:
        uf = {'userId':o for o in userFilters}
        body.user_filters = [buildSimpleAQF(uf, 'or')]
    body.paging = PureCloudPlatformClientV2.PagingSpec()
    body.paging.page_size = 100
    body.paging.page_number = pageNumber
    return body

def buildUserQueryBody(interval,presenceFilters: dict,routingFilters: dict,userFilters: dict, pageNumber = 1):
    body = PureCloudPlatformClientV2.UserDetailsQuery()
    body.interval = interval
    if presenceFilters:
        pf = {k:v for k,v in presenceFilters.items()}
        body.presence_filters = [buildSimpleAQF(pf, 'or')]
    if routingFilters:
        rf = {k:v for k,v in routingFilters.items()}
        body.routing_status_filters = [buildSimpleAQF(rf, 'or')]
    if userFilters:
        uf = {k:v for k,v in userFilters.items()}
        body.user_filters = [buildSimpleAQF(uf, 'or')]
    body.paging = PureCloudPlatformClientV2.PagingSpec()
    body.paging.page_size = 100
    body.paging.page_number = pageNumber
    return body

def buildConversationQueryBody(interval,conversationFilters: list,segmentFilters: list, pageNumber = 1):
    body = PureCloudPlatformClientV2.ConversationQuery()
    body.interval = interval
    if conversationFilters:
        cf = {'systemPresence':o for o in presenceFilters}
        body.conversation_filters = [buildSimpleAQF(f, 'or')]
    if segmentFilters:
        rf = {'routingStatus':o for o in routingFilters}
        body.segment_filters = [buildSimpleAQF(rf, 'or')]
    body.paging = PureCloudPlatformClientV2.PagingSpec()
    body.paging.page_size = 100
    body.paging.page_number = pageNumber
    return body
