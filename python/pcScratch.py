from PureCloudUtils import *
import random
import csv


def getRandomUser():
    return allUsers[random.randint(0,len(allUsers)-1)]

def generateUserReportCsv(userList,properties,filename):
    with open(filename, 'w', newline='') as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(properties)
        for u in userList:
            uOut = flattenUserPropertiesToList(u,properties)
            csvWriter.writerow(uOut)
    

updateToken()

allUsers = getAllUsers()

randUser = getRandomUser()

myFile = "C:\\Users\\mjsmi1\\usersOut.csv"

myProps = ["id",
           "name",
           "email",
           "phoneNumber",
           "title",
           "department",
           "managerName",
           "roleNames",
           "queueNames"
           ]

generateUserReportCsv(allUsers,myProps,myFile)
