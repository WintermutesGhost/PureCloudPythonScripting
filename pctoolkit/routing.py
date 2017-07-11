import PureCloudPlatformClientV2

# Local reference for routing API
routApi = PureCloudPlatformClientV2.apis.RoutingApi()

def getQueues():
    """
    Retrieves list of all pureCloud queue objects in current environment
    
    Limited to ~3000 results
    
    :returns: list of all PureCloud queue objects in current environment
    """
    
    queueList = []
    for page in range(1,30): # TODO: Actually handle pages correctly
        response = routApi.get_routing_queues(page_size=100,page_number=page)
        # Check if last page (empty response)
        if len(response.entities) == 0 : break
        queueList += response.entities
    else:
        raise ValueError('Interval too long: More than 3000 results')
    return queueList
