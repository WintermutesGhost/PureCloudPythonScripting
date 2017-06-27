import PureCloudPlatformClientV2

routApi = PureCloudPlatformClientV2.apis.RoutingApi()

def getQueues():
    queueList = []
    for page in range(1,30): # TODO: Actually handle pages cor
        response = routApi.get_routing_queues(page_size=100,page_number=page)
        if len(response.entities) == 0 : break
        queueList += response.entities
    else:
        raise ValueError('Interval too long: More than 3000 results')
    return queueList
