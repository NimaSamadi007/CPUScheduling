import numpy as np
import matplotlib.pyplot as plt
import RMFP
import EDF

# gets input arguments and flags from the user
def getInputFromUser():
    print("Welcome to RealTime Scheduling software :)")
    numberOfTasks = int(input("Enter the number of tasks: "))
    listOfTasks = []

    CiList = list(map(int, input("Enter C_i for all {} tasks respectively: \n".format(numberOfTasks)).split(" ")))
    TiList = list(map(int, input("Enter T_i for all {} tasks respectively: \n".format(numberOfTasks)).split(" ")))

    for i in range(numberOfTasks):
        listOfTasks.append({
            "C" : CiList[i], 
            "T" : TiList[i], 
        })

    algMethod = input("What scheduling algorithm do you want to use? (RMFP, EDF): ")
    return (listOfTasks, algMethod)

# calculates timing based on the input flags
# and returns one-hot array showing each jobs time
def calProcessorUtilization(listOfTasks, algMethod):
    if algMethod == "RMFP":
        processorUtilization = RMFP.scheduleWithFP(listOfTasks)
    elif algMethod == "EDF":
        processorUtilization = EDF.scheduleWithEDF(listOfTasks)
    else:
        raise ValueError("Unknown scheduling method inserted - must be one of FP, RM, or EDF")

    return processorUtilization

# plots the timing result
def plotResult(timingLists, tasks, algMode):
    width = 2
    fig, ax = plt.subplots()
    yMax = timingLists.shape[0] * 10
    yticksValues = []
    yticksLabels = []
    for i in range(timingLists.shape[0]):
        xRanges = computeXRanges(timingLists[i])
        yRange = (yMax - 10*i, width)
        yticksValues.append(yMax - 10*i + width / 2)
        yticksLabels.append("Task{}".format(i+1))
        ax.broken_barh(xRanges, yRange)
        periodDevidend = calMultiplesOfPeriod(timingLists.shape[1], tasks[i]["T"])
        ax.vlines(x=periodDevidend, ymin = yMax - 10*i - width/2, ymax = yMax - 10*i + 3*width/2, ls='--', colors='red', lw=2)

    ax.set_yticks(yticksValues)
    ax.set_yticklabels(yticksLabels)
    ax.set_xticks(np.arange(0, timingLists.shape[1]+1))
    ax.grid(True)
    ax.set_title('RealTime scheduling by {} method'.format(algMode))
    ax.set_xlabel('Time')
    ax.set_ylabel('Tasks')

    plt.show()

def calMultiplesOfPeriod(totalTime, period):
    periodMultiples = []
    for i in range(totalTime+1):
        if i % period == 0:
            periodMultiples.append(i)
    return periodMultiples

# computing ranges of contigous ones for plotting from the give list
def computeXRanges(inputList):
    oneSeen = False
    startIndex = 0
    length = 0
    xRanges = []
    for i in range(len(inputList)):
        # print(xRanges)
        if not oneSeen and inputList[i] == 1: # first ones is seen:
            oneSeen = True
            startIndex = i
            length += 1
        elif oneSeen and inputList[i] == 1: # another one is seen in the same subarray
            oneSeen = True
            length += 1
        elif oneSeen and inputList[i] == 0: # this was the last 1
            oneSeen = False
            xRanges.append((startIndex, length))
            length = 0
        else: # no one is seen and right now it is zero
            oneSeen = False

    if oneSeen:
        xRanges.append((startIndex, length))

    return xRanges

def convertUtlizationToTiming(procUtilization, numOfTasks):
    timingLists = np.zeros((numOfTasks, len(procUtilization)), dtype=int)
    for i in range(len(procUtilization)):
        timingLists[procUtilization[i]-1, i] = 1
    
    return timingLists

# main function handling whole structure
def main():
    listOfTasks, algMethod = getInputFromUser()
    processorUtilization = calProcessorUtilization(listOfTasks, algMethod)
    timingLists = convertUtlizationToTiming(processorUtilization, len(listOfTasks))
    print("This is how tasks are scheduled: ")
    for i in range(timingLists.shape[0]):
        print("Task{}: ".format(i+1), end=" ")
        print(timingLists[i])
    print("Plotting results...")
    plotResult(timingLists, listOfTasks, algMethod)

if __name__ == "__main__":
    main()
