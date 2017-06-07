import PureCloudPlatformClientV2
import pctoolkit
import csv
import random
import datetime

TMZONE = -6

def updateToken():
    newToken = input("Please enter a new OAUTH token:\n")
    try:
        pctoolkit.oauth.setAccessToken(newToken)
        pctoolkit.users.usersApi.get_users_me()
        print("Authentication successful!")
    except PureCloudPlatformClientV2.rest.ApiException:
        print("Authentication failed")

def flattenUserPropertiesToList(user, propertyList):
    userProperties = []
    for p in propertyList:
        if p == "managerName":
            pValue = pctoolkit.users.getUserManagerName(user)
        elif p == "phoneNumber":
            pValue = pctoolkit.users.extractUserPrimaryPhone(user)
        elif p == "roleNames":
            pValue = ';'.join(pctoolkit.users.getUserRoleNames(user))
        elif p == "queueNames":
            pValue = ';'.join(pctoolkit.users.getUserQueueNames(user))
        else:
            pValue = getattr(user,p)
        userProperties.append(pValue)
    return userProperties

def getRandomUser():
    allUsers = pctoolkit.users.getAllUsers()
    return allUsers[random.randint(0,len(allUsers)-1)]

def generateUserReportCsv(userList,properties,filename):
    with open(filename, 'w', newline='') as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(properties)
        for u in userList:
            uOut = flattenUserPropertiesToList(u,properties)
            csvWriter.writerow(uOut)

def qdump(output,location='C:\\Users\\mjsmi1\\out.txt'):
    with open(location,'w') as outFile:
        try:
            outFile.write(output)
        except TypeError:
            outFile.write(output.to_str())

def getUserIdleIntervals(userId,interval):
    qBody = pctoolkit.analytics.buildPresenceQueryBody(interval,None,["IDLE"],[userId])
    response = pctoolkit.analytics.anaApi.post_analytics_users_details_query(qBody)
    shortIntervals = []
    try:
        routingStatuses = response.user_details[0].routing_status
        for rs in routingStatuses:
            st = (rs.start_time + datetime.timedelta(0,TMZONE)).time().isoformat()
            et = (rs.end_time + datetime.timedelta(0,TMZONE)).time().isoformat()
            shortIntervals.append({'start':st,'end':et})
    except TypeError:
        routingStatuses = None
    return shortIntervals
    


updateToken()
