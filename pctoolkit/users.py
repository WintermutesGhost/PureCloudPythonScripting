import time

import PureCloudPlatformClientV2

# Local reference for users and presence APIs
usersApi = PureCloudPlatformClientV2.apis.UsersApi()
presApi = PureCloudPlatformClientV2.apis.PresenceApi()

def getAllUsers():
    """
    Retrieve a list of all active users in the system
    
    Paginated query, so it is fairly fast
    
    :raises ValueError: only 3000 results supported at a time
    :returns: list of PureCloud user objects
    """
    userList = []
    for page in range(1,30): # Need new pagination function
        response = usersApi.get_users(page_size=100, page_number=page)
        if not response.entities: break
        userList += response.entities
    else:
        raise ValueError('Interval too long: More than 3000 results')
    return userList

def getDeptUsers(deptName):
    """
    Retreieve a list of all active users in a given workgroup
    
    Filters based on whether deptName is found anywhere within the user's
    department field.
    
    :param deptName: text to search in department name field
    :returns: list of matching PureCloud user objects
    """
    allUsers = getAllUsers() #TODO: Use search to avoid pulling all results
    deptUsers = [o for o in allUsers if (o.department is not None and deptName in o.department)]
    return deptUsers

def getUserManagerName(user): #Data writing
    """
    Retrieve name for manager of a given user
    
    Returns blank if no manager is found, or if user object is malformed
    
    :param user: PureCloud user object to extract manager for
    :returns: name of manager
    """
    try:
        managerId = user.manager.id #TODO: Better validation and error handling
        managerName = getUser(managerId).name
    except AttributeError:
        return
    return managerName

def getUserRoleNames(user): #Data writing
    """
    Retrieve list of human readable names for all roles a user has
    
    :param user: PureCloud user object to list roles for
    :returns: list of role names possesed by user
    """
    time.sleep(0.4)
    roles = usersApi.get_user_roles(user.id).roles
    roleNames = [o.name for o in roles]
    return roleNames

def getUserQueueNames(user): #Data writing
    """
    Retrieve list of human readable names for all queues a user is a member of
    
    :param user: PureCloud user object to list queues for
    :returns: list of queue names user is a member of
    """
    time.sleep(0.4)
    queues = usersApi.get_user_queues(user.id).entities
    queueNames = [o.name for o in queues]
    return queueNames



def extractUserPrimaryPhone(user): #Data writing
    """
    Retrieve primary phone number from a user object
    
    Filter is media_type == 'PHONE' & type == 'PRIMARY'
    
    :param user: PureCloud user object to extract phone number from 
    :returns: string with pphone number
    """
    contactInfo = user.primary_contact_info
    phone = None
    for c in contactInfo:
        if ((c.media_type == 'PHONE') & (c.type == 'PRIMARY')):
            phone = c.address
    return phone

def getUser(userId):
    """
    Retrieve PureCloud user object for given userId
    
    :param userId: user id to retrieve
    :returns: PureCloud user object for matching user
    """
    time.sleep(0.4)
    userResult = usersApi.get_user(userId)
    return userResult

def searchUser(searchTerm,searchType='EXACT'):
    """
    Search for user based on id, name, or email
    
    By default, search term must be exact, so retrieved records should be
    unique. If other searchTypes are used then this may not be the case. If 
    multiple results are returned when not enabled, an error is raised to 
    avoid unpredictable results.
    
    :param searchTerm: value to search for (name, is, email)
    :param searchType: how to match search values (EXACT,STARTS_WITH,CONTAINS)
    :returns: PureCloud user object if found, None if no user found
    """
    time.sleep(0.4)
    searchFields = ['name',
                    'email',
                    'id']
    searchBody = { 'query':
                   [{ 'fields':searchFields,
                      'value':searchTerm,
                      'type':searchType }]
                   }
    searchResults = usersApi.post_users_search(searchBody)
    if searchResults.results is None or len(searchResults.results) == 0:
        return None
    if len(searchResults.results) > 1:
        raise ValueError("Retrieved user is not unique. Consider using \
                            searchMultipleUsers instead")
    return searchResults.results[0]

def searchMultipleUsers(searchTerm,searchType='CONTAINS'):
    """
    Search for users based on id, name, or email
    
    Always returns a list, even if a single user is retrieved.
    
    :param searchTerm: value to search for (name, is, email)
    :param searchType: how to match search values (EXACT,STARTS_WITH,CONTAINS) 
    :returns: list of PureCloud user objects found, empty list if no user found
    """
    time.sleep(0.4)
    searchFields = ['name',
                    'email',
                    'id']
    searchBody = { 'query':
                   [{ 'fields':searchFields,
                      'value':searchTerm,
                      'type':searchType }]
                   }
    searchResults = usersApi.post_users_search(searchBody)
    return searchResults.results

def createUser(name,email,password):
    """
    Create a minimal user with given username, email and password
    
    PASSWORD IS NOT HANDLED SAFELY. Do not add user roles before password has 
    been properly changed
    
    :param name: text to add to 'Name' field of new user
    :param email: email address to associate new user with
    :param password: NOT HANDLED SAFELY, password to use for new user
    :returns: completed PureCloud user object for new account
    """
    requestBody = { 'name' : name,
                    'email': email,
                    'password' : password
                    }
    response = usersApi.post_users(requestBody)
    return response

#Incomplete functions. Consider removal TODO: Complete or deprecate

#def assignRoles(userId,roles): #Useful for user management
#    requestBody = roles
#    response = usersApi.put_user_roles(userId,requestBody)
#    return response

#def getUserPresence(user): #Useful for checking surrent user status
#    pass
    
