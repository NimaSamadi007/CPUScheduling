import numpy as np
import utils as utl

def scheduleWithEDF(tasks):
    numOfTasks = len(tasks)
    # check if utilization is less than or equal 1:
    utiliz = utl.calUtilization(tasks)
    if utiliz > 1:
        print("Non-schedulable! utilization is: {}".format(utiliz))
    else:
        print("Processor Utilization: {}".format(utiliz))
    # computing total time to plot
    periods = []
    for t in range(numOfTasks):
        periods.append(tasks[t]["T"])
    totalTime = np.lcm.reduce(periods) # consider LCM as the total time
    issueTimeList = utl.setPeriodsOnAxis(tasks, totalTime)
    issueTimesValues = []
    for i in range(numOfTasks):
        issueTimesValues.append(utl.calMultiplesOfPeriod(totalTime, tasks[i]["T"]))
    issueTimesSet = set([val for sublist in issueTimesValues for val in sublist])

    processorUtilization = np.zeros(totalTime, dtype=int)
    # fill the computation value of each task
    computationValues = np.zeros(numOfTasks, dtype=int)
    for i in range(numOfTasks):
        computationValues[i] = tasks[i]["C"]   
        
    # now schedule processor's cycles
    # print(issueTimeList)
    for t in range(totalTime):
        if t in issueTimesSet: # update priorities
            priorityList = updatePriorities(issueTimesValues, t)
        taskIndex = highestRemainingTask(computationValues, priorityList)
        if taskIndex != -1:
            computationValues[taskIndex] -= 1
            processorUtilization[t] = taskIndex + 1
        utl.updateComputationValues(computationValues, issueTimeList, tasks, t+1)

    return processorUtilization

def updatePriorities(issueTimeVals, currentTime):       
    timeToDeadlines = np.zeros(len(issueTimeVals), dtype=int)
    for i in range(len(issueTimeVals)):
        for v in issueTimeVals[i]:
            if v > currentTime:
                timeToDeadlines[i] = v - currentTime
                break
    return np.argsort(timeToDeadlines) + 1


def highestRemainingTask(computationValues, priorityList):
    for i in range(len(priorityList)):
        taskIndx = priorityList[i]-1
        if computationValues[taskIndx] > 0:
            return taskIndx
    return -1 # no remaining task
