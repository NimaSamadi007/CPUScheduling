import numpy as np

# generates lists of times for each task
# which shows if the task is issued or not (one-hot)
def setPeriodsOnAxis(tasks, totalTime):
    issueTimeList = np.zeros((len(tasks), totalTime+1), dtype=int)
    indices = np.arange(totalTime+1)
    for i in range(len(tasks)):
        issueTimeList[i, indices % tasks[i]["T"] == 0] = 1

    return issueTimeList

