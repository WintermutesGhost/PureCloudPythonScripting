import PureCloudPlatformClientV2
import pctoolkit
import csv
import random
import datetime
import dateutil.parser
import time
import logging

from pctoolkit.analytics import buildSimpleAQF, getConversationsInInterval

TMZONE = -6

def updateToken():
    print("Requesting token")
    newToken = pctoolkit.oauth.requestAccessToken()
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

def getUserRoutingIntervals(userSearchTerm,interval,routingFilter='IDLE'):
    foundUser = pctoolkit.users.searchUser(userSearchTerm)
    userFilter = buildSimpleAQF({'userId':foundUser.id})
    routingFilter = buildSimpleAQF({'routingStatus':routingFilter})
    #if interval == 'TODAY': interval = pctoolkit.core.TODAY
    #if interval == 'YESTERDAY': interval = pctoolkit.core.YESTERDAY
    qBody = pctoolkit.analytics.buildUserQueryBody(interval,None,[routingFilter],[userFilter])
    response = pctoolkit.analytics.anaApi.post_analytics_users_details_query(qBody)
    shortIntervals = []
    try:
        routingStatuses = response.user_details[0].routing_status
        for rs in routingStatuses:
            st = (rs.start_time + datetime.timedelta(0,TMZONE)).time().isoformat()
            et = (rs.end_time + datetime.timedelta(0,TMZONE)).time().isoformat()
            shortIntervals.append({'start':st[:8],'end':et[:8]})
    except TypeError:
        routingStatuses = None
    return shortIntervals

def printShortConvs(convList,minLen=30):
    for conv in convList:
        outId = conv.conversation_id
        for part in conv.participants:
            if part.purpose == 'agent':
                for sess in part.sessions:
                    for seg in sess.segments:
                        if seg.segment_type == 'interact':
                            segS = seg.segment_start
                            segE = seg.segment_end
                            if segE is not None:
                                segDelt = segE - segS
                                if segDelt.seconds < minLen:
                                    print(outId + "  |  " + str(segDelt.seconds))

def printMultiAgentConvs(convList,minCount=2):
    for conv in convList:
        outId = conv.conversation_id
        agentCount = 0
        for part in conv.participants:
            if part.purpose == 'agent':
                agentCount += 1
        if agentCount >= minCount:
            print(outId + "  |  " + str(agentCount))
            
def printRepeatedCallers(convList,minCount=2):
    callerList = {}
    for conv in convList:
        for part in conv.participants:
            if part.purpose == 'external' or part.purpose == 'customer' :
                if part.sessions[0].direction == 'inbound':
                    cPhone = part.sessions[0].ani
                    if cPhone in callerList:
                        callerList[cPhone] += 1
                    else:
                        callerList[cPhone] = 1
    for caller,callCount in callerList.items():
        if callCount >= minCount:
            print("{0}\t\t{1}".format(caller,callCount))

def placeFixedLengthCall(phoneNumber,duration=20):
    openInteraction = pctoolkit.conversations.initiateCallFromMe(phoneNumber)
    print(openInteraction.id)
    if duration > 0:
        time.sleep(duration)
    else:
        input()
    pctoolkit.conversations.terminateInteraction(openInteraction.id)

def placeMultiFixedLengthCall(phoneNumbers,duration=20):
    openInteractions = []
    for pn in phoneNumbers:
        oi = (pctoolkit.conversations.initiateCallFromMe(pn))
        print("open: " , oi.id, "  " , pn)
        openInteractions.append(oi)
        time.sleep(.200)
    if duration > 0:
        time.sleep(duration)
    else:
        input()
    for oi in openInteractions:
        pctoolkit.conversations.terminateInteraction(oi.id)
        print("close:" , oi.id)
        time.sleep(.200)

def printQueueList():
    queues = pctoolkit.routing.getQueues()
    for q in queues:
        print(q.id,"\t",q.name)

def findCallsByParticipantName(participantName,interval):
    calls = pctoolkit.analytics.getConversationsInInterval(interval)
    matchConvs = []
    for call in calls:
        for part in call.participants:
            if part.participant_name == participantName:
                matchConvs.append(call.conversation_id)
                break
    return matchConvs

def findCallsByParticipantList(participantNames,interval):
    calls = pctoolkit.analytics.getConversationsInInterval(interval)
    matchConvs = []
    for call in calls:
        for part in call.participants:
            if part.participant_name in participantNames:
                matchConvs.append(call.conversation_id)
                logging.info('%s agent %s',call.conversation_id,part.participant_name)
                break
    return matchConvs

def retrieveFullConvs(analyticsConvs):
    convIds = [c.conversation_id for c in analyticsConvs]
    fullConvs = []
    processedCount = 0
    convCount = len(convIds)
    processIncrement = 100
    chunkedConvIds = [convIds[x:x+100] for x in range(0,convCount,processIncrement)]
    for convIdsChunk in chunkedConvIds:
        fullConvs += pctoolkit.conversations.getConversationList(convIdsChunk)
        processedCount += processIncrement
        print("\t{0}/{1} complete...".format(processedCount,convCount))
    return fullConvs

def findCallsWithUcid(ucid,interval):
    calls = pctoolkit.analytics.getConversationsInInterval(interval)
    fullConvs = retrieveFullConvs(calls)
    matchConvs = []
    for conv in fullConvs:
        for part in conv.participants:
            if 'ucid' in part.attributes.keys():
                if ucid is None or part.attributes['ucid'] == ucid:
                    matchConvs.append(conv)
                    break
    return matchConvs


updateToken()
