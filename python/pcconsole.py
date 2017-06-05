import pctoolkit
import csv
import random

def updateToken():
    newToken = input("Please enter a new OAUTH token:\n")
    try:
        pctoolkit.oauth.setAccessToken(newToken)
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
    return allUsers[random.randint(0,len(allUsers)-1)]

def generateUserReportCsv(userList,properties,filename):
    with open(filename, 'w', newline='') as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(properties)
        for u in userList:
            uOut = flattenUserPropertiesToList(u,properties)
            csvWriter.writerow(uOut)
