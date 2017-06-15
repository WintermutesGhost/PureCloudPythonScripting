from pcconsole import *

interval = pctoolkit.analytics.YESTERDAY
itscUsers = pctoolkit.users.getDeptUsers('ITSC')
itscIdles = {u.id:getUserIdleIntervals(u.id,interval) for u in itscUsers}
outputTable = []
outputTable.append('[')

for u,t in itscIdles.items():
    for i in t:
        outputTable.append('{"id":"'+u+'","start":"'+i['start']+'","end":"'+i['end']+'"},')

outputTable[-1] = outputTable[-1][:-1]
outputTable.append(']')

with open('C:\\Users\\mjsmi1\\timeOut.txt','w') as outFile:
    for l in outputTable:
        a=outFile.write(l+'\n')

for conv in data['conversations']:
    
