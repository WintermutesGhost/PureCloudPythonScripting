import PureCloudPlatformClientV2
import time

usersApi = PureCloudPlatformClientV2.apis.UsersApi()
presApi = PureCloudPlatformClientV2.apis.PresenceApi()

def getAllUsers():
    userList = usersApi.get_users(page_size = 400)
    return userList.entities

def getDeptUsers(deptName):
    allUsers = getAllUsers()
    deptUsers = [o for o in allUsers if (o.department is not None and deptName in o.department)]
    return deptUsers

def getUserManagerName(user):
    try:
        managerId = user.manager.id
        managerName = getUser(managerId)
    except AttributeError:
        return
    return managerName

def getUserRoleNames(user):
    time.sleep(0.4)
    roles = usersApi.get_user_roles(user.id).roles
    roleNames = [o.name for o in roles]
    return roleNames

def getUserQueueNames(user):
    time.sleep(0.4)
    queues = usersApi.get_user_queues(user.id).entities
    queueNames = [o.name for o in queues]
    return queueNames

def getUserPresence(user):
    pass

def extractUserPrimaryPhone(user):
    contactInfo = user.primary_contact_info
    phone = None
    for c in contactInfo:
        if ((c.media_type == 'PHONE') & (c.type == 'PRIMARY')):
            phone = c.address
    return phone

def getUser(searchTerm):
    time.sleep(0.4)
    searchFields = ['name',
                    'email',
                    'id']
    searchBody = { 'query':
                   [{ 'fields':searchFields,
                      'value':searchTerm,
                      'type':'EXACT' }]
                   }
    searchResults = usersApi.post_users_search(searchBody)
    if len(searchResults.results) == 0:
        return None
    return searchResults.results[0]

def createUser(name,password):
    email = name + '@ucalgary.ca'
    requestBody = { 'name' : name,
                    'email': email,
                    'password' : password
                    }
    response = usersApi.post_users(requestBody)
    return response

def assignRoles(userId,roles):
    requestBody = roles
    response = usersApi.put_user_roles(userId,requestBody)
    return response

def makeBasicRtcUser(name,password):
    userResponse = createUser(name,password)
    print("User created: " + userResponse.name + "/" + userResponse.id)
    rolesResponse = assignRoles(userResponse.id,[ROLEEMP,ROLECOMM])
    print("Roles assigned")
    #teleResponse = createWebRtc(userResponse.id)
    #print(teleResponse)

def checkUserStatus(user):
    pass
    
