import PureCloudPlatformClientV2
import datetime
#from pctoolkit.core import buildSimpleAQF,TODAY,YESTERDAY 

anaApi = PureCloudPlatformClientV2.apis.AnalyticsApi()

#TODO: Make these timesone-aware

TODAY = datetime.date.today().isoformat() \
        +"T00:00:00Z/" \
        +(datetime.date.today() + datetime.timedelta(1)).isoformat() \
        +"T00:00:00Z" #deprecated

YESTERDAY = (datetime.date.today() - datetime.timedelta(1)).isoformat() \
        +"T00:00:00Z/" \
        +datetime.date.today().isoformat() \
        +"T00:00:00Z" #deprecated

def dayInterval(dateStr): #deprecated
    timestamp = "{0}T00:00:00Z/{0}T23:59:59Z".format(dateStr)
    return timestamp

def makeInterval(startDate,length = 1):
    sy = int(startDate[0:4])
    sm = int(startDate[5:7])
    sd = int(startDate[8:10])
    startDatetime = datetime.date(sy,sm,sd)
    endDatetime = startDatetime + datetime.timedelta(days=length)
    endDate = endDatetime.isoformat()
    timestamp = "{0}T00:00:00Z/{1}T00:00:00Z".format(startDate,endDate)
    return timestamp
#    timestamp = "{0}T00:00:00Z/{0}T23:59:59Z".format(dateStr)
#    return timestamp

def buildSimpleAQF(predicates: dict, filterType = 'and'):
    aqFilter = PureCloudPlatformClientV2.AnalyticsQueryFilter()
    aqFilter.predicates = []
    if ((filterType != 'and') and (filterType != 'or')):
        raise ValueError("Invalid filterType, must be 'and'/'or'")
    aqFilter.type = filterType
    for dimension,value in predicates.items():
        aqFilter.predicates.append(PureCloudPlatformClientV2.AnalyticsQueryPredicate())
        aqFilter.predicates[-1].dimension = dimension
        if (value == 'exists') or (value == 'notExists'):
            aqFilter.predicates[-1].operator = value
        else:
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

def getConversationsInInterval(interval):
    query = buildConversationQueryBody(interval,None,None)
    convList = postPaginatedConvQuery(query)
    return convList

def getConversationsByStatus(interval,statusFilter):
    convPred = None
    segPred = None
    if statusFilter == 'talking':
        convPred = {'conversationEnd':'notExists'}
    #elif statusfilter == 'live':
    #    segPred = {'
    elif statusFilter == 'wrappingUp':
        convPred = {'conversationEnd':'exists'}
        segPred = {'wrapUpCode':'notExists','purpose':'agent','segmentType':'wrapup'}
    elif statusFilter == 'ended':
        convPred = {'conversationEnd':'exists'}
        segPred = {'wrapUpCode':'exists'}
    else:
        raise ValueError('Invalid statusFilter')
    convFilt = [buildSimpleAQF(convPred)] if convPred else None
    segFilt = [buildSimpleAQF(segPred)] if segPred else None
    query = buildConversationQueryBody(interval,convFilt,segFilt)
    convList = postPaginatedConvQuery(query)
    return convList
    
def postPaginatedConvQuery(query):
    convList = []
    for page in range(1,100):
        query.paging.page_number = page
        response = anaApi.post_analytics_conversations_details_query(query)
        if response.conversations is None: break
        convList += response.conversations
    else:
        raise ValueError('Interval too long: More than 10000 results')
    return convList
