import PureCloudPlatformClientV2
import time

usersApi = PureCloudPlatformClientV2.apis.UsersApi()

def updateToken():
    newToken = input("Please enter a new OAUTH token:\n")
    try:
        setAccessToken(newToken)
        print("Authentication successful!")
    except PureCloudPlatformClientV2.rest.ApiException:
        print("Authentication failed")

def setAccessToken(newToken):
    PureCloudPlatformClientV2.configuration.access_token = newToken
    usersApi.get_users_me()
    
def getAllUsers():
    userList = usersApi.get_users(page_size = 400)
    return userList.entities

def flattenUserPropertiesToList(user, propertyList):
    userProperties = []
    for p in propertyList:
        if p == "managerName":
            pValue = getUserManagerName(user)
        elif p == "phoneNumber":
            pValue = extractUserPrimaryPhone(user)
        elif p == "roleNames":
            pValue = ';'.join(getUserRoleNames(user))
        elif p == "queueNames":
            pValue = ';'.join(getUserQueueNames(user))
        else:
            pValue = getattr(user,p)
        userProperties.append(pValue)
    return userProperties

def getUserManagerName(user):
    try:
        managerId = user.manager.id
        managerName = getNameFromId(managerId)
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

def extractUserPrimaryPhone(user):
    contactInfo = user.primary_contact_info
    phone = None
    for c in contactInfo:
        if ((c.media_type == 'PHONE') & (c.type == 'PRIMARY')):
            phone = c.address
    return phone

def getNameFromId(lookupId):
    time.sleep(0.4)
    user = usersApi.get_user(lookupId)
    return user.name

def addManagerName(user):
    try:
        managerId = user.manager.id
        managerName = getNameFromId(managerId)
    except AttributeError:
        return
    setattr(user,"managerName",managerName)

#def addQueueNameList(
