from pctoolkit.users import getUserManagerName,extractUserPrimaryPhone,getUserRoleNames,getUserQueueNames

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
