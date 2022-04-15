import numpy as np

# generates lists of times for each task
# which shows if the task is issued or not (one-hot)
def setPeriodsOnAxis(tasks, totalTime):
    issueTimeList = np.zeros((len(tasks), totalTime+1), dtype=int)
    indices = np.arange(totalTime+1)
    for i in range(len(tasks)):
        issueTimeList[i, indices % tasks[i]["T"] == 0] = 1

    return issueTimeList

def calMultiplesOfPeriod(totalTime, period):
    periodMultiples = []
    for i in range(totalTime+1):
        if i % period == 0:
            periodMultiples.append(i)
    return periodMultiples

def updateComputationValues(computationValues, issueTimeList, tasks, time):
    for i in range(len(tasks)):
        if issueTimeList[i, time] == 1: # Task i is issueing at "time"
            computationValues[i] += tasks[i]["C"]

def calUtilization(tasks):
    utilization = 0
    for i in range(len(tasks)):
        utilization += (tasks[i]["C"] / tasks[i]["T"])
    return utilization