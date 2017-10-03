import PureCloudPlatformClientV2

# Local reference for routing API
routApi = PureCloudPlatformClientV2.apis.RoutingApi()

def getQueues():
    """
    Retrieve a list of all pureCloud queue objects in current environment
    
    Limited to ~3000 results
    
    :raises ValueError: lists of queue too long, only 3000 results supported
    :returns: list of all PureCloud queue objects in current environment
    """
    queueList = []
    for page in range(1,30): # TODO: Unify pages functionality
        response = routApi.get_routing_queues(page_size=100,page_number=page)
        # Check if last page (empty response)
        if len(response.entities) == 0 : break
        queueList += response.entities
    else:
        raise ValueError('Interval too long: More than 3000 results')
    return queueList

def getWrapupCodes():
    wrapupList = []
    for page in range(1,30):
        response = routApi.get_routing_wrapupcodes(page_size=100,page_number=page)
        # Check if last page (empty response)
        if len(response.entities) == 0 : break
        wrapupList += response.entities
    else:
        raise ValueError('Interval too long: More than 3000 results')
    return wrapupList

def getQueueWrapupCodes(queueId):
    wrapupList = []
    for page in range(1,30):
        response = routApi.get_routing_queue_wrapupcodes(queueId,
                                                         page_size=100,
                                                         page_number=page)
        if len(response.entities) == 0: break
        wrapupList += response.entities
    else:
        raise ValueError('Interval too long: More than 3000 results')
    return wrapupList