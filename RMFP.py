import math
import utils as utl
import numpy as np

# I assume that at most in MAX_NUM_OF_ITERATION the algorithm
# will converges to a value. If not, the tasks are not schedulable
MAX_NUM_OF_ITERATION = 10000

# Schedules tasks using fixed priotiry.
# This function assumes that the lower index tasks are
# having higher priority. For instances task with index=1
# has the highest priority among others.
def scheduleWithFP(tasks):
    numOfTasks = len(tasks)
    # Find the response time of the lowest priority task
    totalTime = calResposeTime(numOfTasks-1, tasks)
    if totalTime == -1:
        print("Non-Schedulable! Examine the timing plot")
        periods = []
        for t in range(numOfTasks):
            periods.append(tasks[t]["T"])
        totalTime = np.lcm.reduce(periods) # consider LCM as the total time
    elif totalTime > tasks[numOfTasks-1]["T"]: # response time exceeds the issue time
        print("Non-Schedulable! Examine the timing plot")

    # compute issue times and set them on the time axis
    issueTimeList = utl.setPeriodsOnAxis(tasks, totalTime)
    processorUtilization = np.zeros(totalTime, dtype=int)

    computationValues = np.zeros(numOfTasks, dtype=int)
    for i in range(numOfTasks):
        computationValues[i] = tasks[i]["C"]   

    for t in range(totalTime):
        taskIndex = highestRemainingTask(computationValues)
        computationValues[taskIndex] -= 1 # subtract 1 computation unit
        processorUtilization[t] = taskIndex + 1 # At time t, task "taskIndex + 1" must be run
        updateComputationValues(computationValues, issueTimeList, tasks, t+1) # update computationValues for next iteration

    return processorUtilization

def updateComputationValues(computationValues, issueTimeList, tasks, time):
    for i in range(len(tasks)):
        if issueTimeList[i, time] == 1: # Task i is issueing at "time"
            computationValues[i] += tasks[i]["C"]

def highestRemainingTask(computationValues):
    for i in range(len(computationValues)):
        if computationValues[i] > 0:
            return i
    return -1 # no remaining task

def calResposeTime(index, tasks):
    responseTime = tasks[index]["C"]
    for i in range(index):
        responseTime += tasks[i]["C"]

    # compute response time iteratively
    iterIndex = 0
    while(1):
        newResponseTime = tasks[index]["C"]
        for i in range(index):
            newResponseTime += (math.ceil(responseTime / tasks[i]["T"])) * tasks[i]["C"]
        iterIndex += 1        
        if newResponseTime - responseTime == 0:
            return newResponseTime
        elif iterIndex >= MAX_NUM_OF_ITERATION: # Non-schedulable
            return -1
        else:
            responseTime = newResponseTime

