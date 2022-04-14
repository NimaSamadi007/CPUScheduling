from Algorithms.EDF import scheduleWithEDF
from Algorithms.FP import scheduleWithFP
from Algorithms.RM import scheduleWithRM

# gets input arguments and flags from the user
def getInputFromUser():
    print("Welcome to RealTime Scheduling software :)")
    numberOfTasks = int(input("Enter the number of tasks: "))
    listOfTasks = []

    CiList = list(map(int, input("Enter C_i for all {} tasks respectively: \n".format(numberOfTasks)).split(" ")))
    TiList = list(map(int, input("Enter T_i for all {} tasks respectively: \n".format(numberOfTasks)).split(" ")))
    DiList = list(map(int, input("Enter D_i for all {} tasks respectively: \n".format(numberOfTasks)).split(" ")))

    for i in range(numberOfTasks):
        listOfTasks.append({
            "C" : CiList[i], 
            "T" : TiList[i], 
            "D" : DiList[i]
        })

    algMethod = input("What scheduling algorithm do you want to use? (FP, RM, EDF): ")
    return (listOfTasks, algMethod)

# calculates timing based on the input flags
# and returns one-hot array showing each jobs time
def calTiming(listOfTasks, algMethod):
    if algMethod == "FP":
        timingLists = scheduleWithFP(listOfTasks)
    elif algMethod == "RM":
        timingLists = scheduleWithRM(listOfTasks)
    elif algMethod == "EDF":
        timingLists = scheduleWithEDF(listOfTasks)
    else:
        raise ValueError("Unknown scheduling method inserted - must be one of FP, RM, or EDF")

    return timingLists

# plots the timing result
def plotResult(timingLists):
    pass

# main function handling whole structure
def main():
    listOfTasks, algMethod = getInputFromUser()
    timingLists = calTiming(listOfTasks, algMethod)
    plotResult(timingLists)

######
# SIMPLE TEST:
# C_i = [2, 2, 5]
# T_i = [5, 9, 20]
# D_i = [3, 6, 5]
######

if __name__ == "__main__":
    main()
