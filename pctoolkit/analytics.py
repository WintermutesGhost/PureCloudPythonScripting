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


def buildUserQueryBody(interval,presenceFilters: list,routingFilters: list,userFilters: list, pageNumber = 1):
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
    body.paging.page_number = pageNumber
    return body

def buildConversationQueryBody(interval,conversationFilters: list,segmentFilters: list, pageNumber = 1):
    body = PureCloudPlatformClientV2.ConversationQuery()
    body.interval = interval
    if conversationFilters:
        body.conversation_filters = conversationFilters
    if segmentFilters:
        body.segment_filters = segmentFilters
    body.paging = PureCloudPlatformClientV2.PagingSpec()
    body.paging.page_size = 100
    body.paging.page_number = pageNumber
    return body


