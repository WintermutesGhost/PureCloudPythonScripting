from PureCloudUtils import *
import random
import csv
import os


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

myDir = os.path.dirname(os.path.abspath(__file__))
print("dir: " + myDir)

myFile = "/usersOut.csv"
print("file: " + myFile)

myPath = os.path.join(myDir, myFile)
print("path: " + myPath)

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

generateUserReportCsv(allUsers,myProps,myPath)
