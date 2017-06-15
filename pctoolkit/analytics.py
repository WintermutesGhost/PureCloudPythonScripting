import PureCloudPlatformClientV2
from pctoolkit.core import buildSimpleAQF,TODAY,YESTERDAY 

anaApi = PureCloudPlatformClientV2.apis.AnalyticsApi()

#TODO: Make these timesone-aware

TODAY = datetime.date.today().isoformat() \
        +"T00:00:00Z/" \
        +(datetime.date.today() + datetime.timedelta(1)).isoformat() \
        +"T00:00:00Z"

YESTERDAY = (datetime.date.today() - datetime.timedelta(1)).isoformat() \
        +"T00:00:00Z/" \
        +datetime.date.today().isoformat() \
        +"T00:00:00Z"

def buildSimpleAQF(predicates: dict, filterType = 'and'):
    aqFilter = PureCloudPlatformClientV2.AnalyticsQueryFilter()
    aqFilter.predicates = []
    if ((filterType != 'and') and (filterType != 'or')):
        raise ValueError("Invalid filterType, must be 'and'/'or'")
    aqFilter.type = filterType
    for dimension,value in predicates.items():
        aqFilter.predicates.append(PureCloudPlatformClientV2.AnalyticsQueryPredicate())
        aqFilter.predicates[-1].dimension = dimension
        aqFilter.predicates[-1].value = value
    return aqFilter


def buildPresenceQueryBody(interval,presenceFilters: list,routingFilters: list,userFilters: list, pageNumber = 1):
    body = PureCloudPlatformClientV2.UserDetailsQuery()
    body.interval = interval
    if presenceFilters:
        body.presence_filters = presenceFilters
    if routingFilters:
        body.routing_status_filters = routingFilters
    if userFilters:
        body.user_filters = userFilters
    body.paging = PureCloudPlatformClientV2.PagingSpec()
    body.paging.page_size = 100
    body.paging.page_number = pageNumber #TODO: Better paging?
    return body

def buildUserQueryBody(interval,presenceFilters: dict,routingFilters: dict,userFilters: dict, pageNumber = 1):
    body = PureCloudPlatformClientV2.UserDetailsQuery()
    body.interval = interval
    if presenceFilters:
        pf = {k:v for k,v in presenceFilters.items()} #TODO:Put in right filters
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
        cf = {'systemPresence':o for o in presenceFilters} #TODO: Put in right filters
        body.conversation_filters = [buildSimpleAQF(f, 'or')]
    if segmentFilters:
        rf = {'routingStatus':o for o in routingFilters}
        body.segment_filters = [buildSimpleAQF(rf, 'or')]
    body.paging = PureCloudPlatformClientV2.PagingSpec()
    body.paging.page_size = 100
    body.paging.page_number = pageNumber
    return body


