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



from ortools.sat.python import cp_model
import math
import random


def numberOfConcurrentMeetings(gMin, n):
    return math.ceil(n / gMin)


def generateRandomSpecificT(n, m, d):
    specificT = []
    for i in range(n):
        outerList = []
        for j in range(d):
            innerList = []
            for k in range(m):
                 # innerList.append(random.randint(0, 1))
                if random.random() < 0.5:
                    if random.random() < 0.2:
                        innerList.append(1)
                    else:
                        innerList.append(0)       
                else:
                    if random.random() < 0.5:
                        innerList.append(1)
                    else:
                        innerList.append(0)        
            outerList.append(innerList)
        specificT.append(outerList)
    return specificT


def maximizeTotalPeople(specificT, people, meetings, days, gMin, gMax, printOutput = False, returnTime = True, returnAllValues = False):
    n = people
    m = meetings
    d = days
    possibleConcurrentMeetings = numberOfConcurrentMeetings(gMin, n)

    all_people = range(n)
    all_shifts = range(m)
    all_days = range(d)
    all_concurrent_meetings = range(possibleConcurrentMeetings)


    # Creates the model.
    model = cp_model.CpModel()

    shifts = {}
    for n in all_people:
        for d in all_days:
            for s in all_shifts:
                for c in all_concurrent_meetings:
                    shifts[(n, d,
                        s, c)] = model.NewBoolVar('shift_%i%i%i%i' % (n, d, s, c))

    # Each person can attend at most 1 meeting per day
    for n in all_people:
        for d in all_days:
            model.Add(sum([shifts[(n, d, s, c)] for s in all_shifts for c in all_concurrent_meetings]) <= 1)

    # Each meeting must have either 0 or between g_min and g_max attendees
    possibleValues = [] # values which meeting size can sum to
    possibleValues.append([0])
    for i in range(gMin, gMax + 1, 1):
        possibleValues.append([i])

    for d in all_days:
        for s in all_shifts:
            for c in all_concurrent_meetings:
                thisSum = model.NewIntVar(0, gMax, 'sum%i%i%i' % (d, s, c))
                model.Add(thisSum == sum(shifts[(n, d, s, c)] for n in all_people))
                model.AddAllowedAssignments([thisSum], possibleValues)


    
    # Apply each person's unavailabilities
    for n in all_people:
        for d in all_days:
            for s in all_shifts:
                for c in all_concurrent_meetings:
                    if specificT[n][d][s] == 0:
                        model.Add(shifts[(n, d, s, c)] == 0)


    model.Maximize(
        sum(shifts[(n, d, s, c)] for n in all_people
            for d in all_days for s in all_shifts for c in all_concurrent_meetings))
    solver = cp_model.CpSolver()
    solver.Solve(model)

    if printOutput:
        for d in all_days:
            for s in all_shifts:
                for c in all_concurrent_meetings:
                    if sum(solver.Value(shifts[(n, d, s, c)]) for n in all_people) == 0:
                        continue
                    print('Day #' + str(d) + ' Shift #' + str(s) + ' Meeting #' + str(c) + ' Attendees:')
                    for n in all_people:
                        if solver.Value(shifts[(n, d, s, c)]) == 1:
                            print('Person #' + str(n))
                    print()

        print()
        print('  - wall time       : %f s' % solver.WallTime())
    
    if returnAllValues:
        fullMatrix = []
        for d in all_days:
            dayList = []
            for s in all_shifts:
                shiftList = []
                for c in all_concurrent_meetings:
                    concurrentList = []
                    for n in all_people:
                        if solver.Value(shifts[(n, d, s, c)]) == 1:
                            concurrentList.append(1)
                        else:
                            concurrentList.append(0)
                    shiftList.append(concurrentList)
                dayList.append(shiftList)
            fullMatrix.append(dayList)
        return fullMatrix 
                            

    if returnTime:
        return solver.WallTime()


if __name__ == '__main__':  
    # specificT = [
    # [[1, 1], [0, 1], [0, 0], [0, 1], [1, 0]],
    # [[1, 0], [1, 1], [0, 1], [0, 1], [0, 0]],
    # [[0, 0], [1, 0], [1, 1], [1, 0], [0, 1]],
    # [[1, 0], [0, 1], [0, 1], [1, 0], [1, 1]]
    # ]
    # n = 4
    # m = 2
    # d = 5
    # gMin = 2
    # gMax = 4
    # maximizeTotalPeople(specificT, n, m, d, gMin, gMax, printOutput=True, returnTime = False, returnAllValues=True)
    n = 10
    m = 2
    d = 20
    gMin = 4
    gMax = 10
    maximizeTotalPeople(generateRandomSpecificT(n, m, d), n, m, d, gMin, gMax, printOutput=True)