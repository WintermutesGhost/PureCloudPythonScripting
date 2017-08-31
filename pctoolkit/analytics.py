import datetime

import PureCloudPlatformClientV2

# Local reference for analytics API
anaApi = PureCloudPlatformClientV2.apis.AnalyticsApi()


def daysInterval(startDate,intervalLength = 1):
    """
    Generate a formatted interval string spanning a number of days
    
    Generate a PureCloud Analytics string spanning an interval of several
    days, between 00:00:00 UTC to 00:00:00 UTC
    
    :param startDate: datestamp to start the interval at ("YYYY-MM-DD")
    :param intervalLength: total days to span, default 1 is the startDate only
    :returns: formatted Purecloud interval string
    :raises ValueError: startDate cannot be parsed into datetime
    """
    # Break datestamp into parts
    # TODO: Use datetime for handling of inputed date
    # TODO: Timezone awareness for intervals
    # Can datetime do this more reliably?
    try:
        sy = int(startDate[0:4])
        sm = int(startDate[5:7])
        sd = int(startDate[8:10])
    except ValueError:
        raise ValueError("Could not parse startDate, should be 'YYYY-MM-DD'")
    # Parse start and end datetime objects
    startDatetime = datetime.date(sy,sm,sd)
    endDatetime = startDatetime + datetime.timedelta(days=intervalLength)
    endDate = endDatetime.isoformat()
    # Final formatting to match PureCloud's format
    timestamp = "{0}T00:00:00Z/{1}T00:00:00Z".format(startDate,endDate)
    return timestamp

def buildSimpleAQF(predicates:dict, filterType='and'):
    """
    Builds a minimal filter for use with PureCloud Analytics Query Filters
    
    Queries are limited to a set list of predicate field/values joined
    by the filterType. Predicate values can also be 'exists' or 'notExists'
    to check for existence/non-existence of the field
    
    TODO: examples
    
    :param predicates: dict of {field:value} to filter on
    :param filterType: how to combine filters (and/or)
    :returns: completed AnalyticsQueryFilter object with predicate fitlers
    :raises ValueError: filter type can only be 'and'/'or'
    """
    aqFilter = PureCloudPlatformClientV2.AnalyticsQueryFilter()
    # Assign filter type for how to join predicates 
    aqFilter.predicates = []
    if ((filterType != 'and') and (filterType != 'or')):
        raise ValueError("Invalid filterType, must be 'and'/'or'")
    aqFilter.type = filterType
    # Iterate through the desired filter predicates and add them to the filter
    for dimension,value in predicates.items():
        aqFilter.predicates.append(PureCloudPlatformClientV2
                                   .AnalyticsQueryPredicate())
        aqFilter.predicates[-1].dimension = dimension
        # Check for special value filters 'exists' and 'notExists'
        if (value == 'exists') or (value == 'notExists'):
            aqFilter.predicates[-1].operator = value
        else:
            aqFilter.predicates[-1].value = value
    return aqFilter

def buildUserQueryBody(interval, presenceFilters:list, routingFilters:list,
                       userFilters:list, pageNumber=1):
    """
    Builds a ready-to-send query body for User Analytics
    
    Arbitrary filters can be added through the presence, routing and user
    filter attributes. They must be a list of fully formed Objects of the 
    PureCloud AnalyticsQueryPredicate class.
    
    :param interval: formatted PureCloud interval string to search
    :param presenceFilters: list of AQPredicates to filter by presences 
    :param routingFilters: list of AQPredicates to filter by routing
    :param userFilters: list of AQPredicates to filter by users
    :param pageNumber: page number to retrieve
    :returns: completed UserDetailQuery object to send as body of a query
    """
    body = PureCloudPlatformClientV2.UserDetailsQuery()
    body.interval = interval
    # Attach filters
    body.presence_filters = presenceFilters
    body.routing_status_filters = routingFilters
    body.user_filters = userFilters
    # Build Paging
    body.paging = PureCloudPlatformClientV2.PagingSpec()
    body.paging.page_size = 100
    body.paging.page_number = pageNumber
    return body

def buildConversationQueryBody(interval, conversationFilters:list,
                               segmentFilters:list, pageNumber=1):
    """
    Builds a ready-to-send query body for Conversation Analytics
    
    Arbitrary filters can be added through the conversation and segment
    filter attributes. They must be a list of fully formed Objects of the 
    PureCloud AnalyticsQueryPredicate class.
    
    :param interval: formatted PureCloud interval string to search
    :param conversationFilters: list of AQPredicates to filter by conversations 
    :param segmentFilters: list of AQPredicates to filter by segments
    :param pageNumber: page number to retrieve
    :returns: completed UserDetailQuery object to send as body of a query
    """
    body = PureCloudPlatformClientV2.ConversationQuery()
    body.interval = interval
    # Attach filters
    body.conversation_filters = conversationFilters
    body.segment_filters = segmentFilters
    # Build paging
    body.paging = PureCloudPlatformClientV2.PagingSpec()
    body.paging.page_size = 100
    body.paging.page_number = pageNumber
    return body

def getConversationsInInterval(interval):
    """
    Retrieves a list of all conversations in an interval
    
    :param interval: formatted PureCloud interval string to search
    :returns: list of PureCloud analytics conversation detail objects
    """
    query = buildConversationQueryBody(interval,None,None)
    convList = postPaginatedConvQuery(query)
    return convList

def getConversationsByStatus(interval,statusFilter):
    """
    Retrieves a list of all conversations in a current status
    
    Currently defined conversation statuses are 'talking' (conversation has
    not ended), 'wrappingUp' (conversation has ended, but no wrap up code),
    'ended' (conversation had ended, and wrapup code exists)
    
    :param interval: formatted PureCloud interval string to search
    :param statusFilter: status name to filter by
    :returns: list of PureCloud analytics conversation detail objects
    :raises ValueError: statusFilter is not one of the valid choices
    """
    convPred = None
    segPred = None
    # Filter type definitions, with dict of predicates needed to filter
    # TODO: Extract this to separate data object
    if statusFilter == 'openLine':
        segPred = {'segmentEnd':'notExists','segmentType':'interact'}
    elif statusFilter == 'open':
        convPred = {'conversationEnd':'notExists'}
    elif statusFilter == 'wrappingUp':
        convPred = {'conversationEnd':'exists'}
        segPred = {'wrapUpCode':'notExists','purpose':'agent','segmentType':'wrapup'}
    elif statusFilter == 'ended':
        convPred = {'conversationEnd':'exists'}
        segPred = {'wrapUpCode':'exists'}
    else:
        raise ValueError('Invalid statusFilter')
    # Avoid sending lists of None, only build lists if we need the filter
    convFilt = [buildSimpleAQF(convPred)] if (convPred is not None) else None
    segFilt = [buildSimpleAQF(segPred)] if (segPred is not None) else None
    query = buildConversationQueryBody(interval,convFilt,segFilt)
    convList = postPaginatedConvQuery(query)
    return convList
    
def postPaginatedConvQuery(query): #Move to core with general purpose querier
    """
    Post a paged query and retrieve page-by-page, concatenating results
    
    Note that this ignores the existing page set in the query
    
    :param query: fully formed PureCloud analytics query body
    :returns: list of PureCloud analytics conversation detail objects
    :raises LookupError: number of retrieved pages is too high (200)
    """
    convList = []
    for page in range(1,200):
        query.paging.page_number = page
        response = anaApi.post_analytics_conversations_details_query(query)
        # Check if we retreived an empty page
        if response.conversations is None: break
        convList += response.conversations
    else:
        raise LookupError('Interval too long: More than 10000 results')
    return convList
