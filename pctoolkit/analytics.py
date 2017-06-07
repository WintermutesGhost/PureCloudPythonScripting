import PureCloudPlatformClientV2
import datetime

anaApi = PureCloudPlatformClientV2.apis.AnalyticsApi()



TODAY = datetime.date.today().isoformat() \
        +"T00:00:00Z/" \
        +(datetime.date.today() + datetime.timedelta(1)).isoformat() \
        +"T00:00:00Z"

YESTERDAY = (datetime.date.today() - datetime.timedelta(1)).isoformat() \
        +"T00:00:00Z/" \
        +datetime.date.today().isoformat() \
        +"T00:00:00Z"

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

        
def buildSimpleAQF(predicates: dict, filterType = 'and'):
    aqFilter = PureCloudPlatformClientV2.AnalyticsQueryFilter()
    aqFilter.predicates = []
    if ((filterType != 'and') and (filterType != 'or')):
        raise ValueError("Invalid filterType, must be 'and'/'or'")
    aqFilter.type = filterType
    #if type(predicates) is not dict: #Don't typecheck in Python?
    #    raise ValueError("Invalid predicates, must be a dict of {dimension:value}")
    for dimension,value in predicates.items():
        aqFilter.predicates.append(PureCloudPlatformClientV2.AnalyticsQueryPredicate())
        aqFilter.predicates[-1].dimension = dimension
        aqFilter.predicates[-1].value = value
    return aqFilter


