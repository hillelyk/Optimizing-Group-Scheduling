# Copyright 2021 Hillel Koslowe

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



import csv
from maximizeTotalAttendees import maximizeTotalPeople, generateRandomSpecificT
from maximizeNewPeopleMet import maximizeNewPeople

with open('schedulingTemplate.csv', 'r') as thisFile:
    thisFile.readline()
    header = thisFile.readline().split(',')
    n = int(header[1])
    d = int(header[2])
    m = int(header[3])
    gMin = int(header[4])
    gMax = int(header[5])
    objective = header[6]

    thisFile.readline()
    dateRow = thisFile.readline().split(',')
    dates = [dateRow[i] for i in range(2, d * m + 2, m)]

    timeRow = thisFile.readline().split(',')
    times = [timeRow[i] for i in range(2, len(timeRow))]
    times[-1] = times[-1].split('\n')[0] # gets rid of new line character in last times

    thisFile.readline()
    thisFile.readline()
    names = []
    specificT = []
    for i in range(n):
        thisPerson = thisFile.readline().split(',')
        names.append(thisPerson[1])
        personList = []
        for j in range(d):
            dayList = []
            for k in range(m):
                if len(thisPerson[j * m + k + 2]) > 0 and thisPerson[j * m + k + 2] != '\n':
                    dayList.append(1)
                else:
                    dayList.append(0)
            personList.append(dayList)
        specificT.append(personList)
    
if objective.strip().lower() == 'new':
    fullSchedule = maximizeNewPeople(specificT, n, m, d, gMin, gMax, printOutput=True, returnAllValues=True)
else:
    fullSchedule = maximizeTotalPeople(specificT, n, m, d, gMin, gMax, printOutput=True, returnAllValues=True)

def dim(a):
    if type(a) != list:
        return []
    return [len(a)] + dim(a[0])

dimensions = dim(fullSchedule)

with open('outputTemplate.csv', 'w') as writeFile:
    withBlanks = ['Date', 'Time']
    withBlanks.extend(names)
    writer = csv.DictWriter(writeFile, fieldnames = withBlanks)
    writer.writeheader()

    days = dimensions[0]
    meetingTimes = dimensions[1]
    concurrentMeetings = dimensions[2]
    attendance = dimensions[3]

    for d in range(days):
        for m in range(meetingTimes):
            for c in range(concurrentMeetings):
                if sum(fullSchedule[d][m][c]) == 0: # nobody attends this meeting
                    continue
                row = {}
                row['Date'] = dates[d]
                row['Time'] = times[d * meetingTimes + m]
                for person in range(attendance):
                    if fullSchedule[d][m][c][person] == 1:
                        row[names[person]] = 1
                writer.writerow(row)




    

