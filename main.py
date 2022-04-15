import numpy as np
import matplotlib.pyplot as plt
import FP
import RM
import EDF

# gets input arguments and flags from the user
def getInputFromUser():
    print("Welcome to RealTime Scheduling software :)")
    numberOfTasks = int(input("Enter the number of tasks: "))
    listOfTasks = []

    CiList = list(map(int, input("Enter C_i for all {} tasks respectively: \n".format(numberOfTasks)).split(" ")))
    TiList = list(map(int, input("Enter T_i for all {} tasks respectively: \n".format(numberOfTasks)).split(" ")))
    #DiList = list(map(int, input("Enter D_i for all {} tasks respectively: \n".format(numberOfTasks)).split(" ")))

    for i in range(numberOfTasks):
        listOfTasks.append({
            "C" : CiList[i], 
            "T" : TiList[i], 
#            "D" : DiList[i]
            "D" : 0
        })

#    algMethod = input("What scheduling algorithm do you want to use? (FP, RM, EDF): ")
    algMethod = "FP"
    return (listOfTasks, algMethod)

# calculates timing based on the input flags
# and returns one-hot array showing each jobs time
def calProcessorUtilization(listOfTasks, algMethod):
    if algMethod == "FP":
        processorUtilization = FP.scheduleWithFP(listOfTasks)
    elif algMethod == "RM":
        processorUtilization = RM.scheduleWithRM(listOfTasks)
    elif algMethod == "EDF":
        processorUtilization = EDF.scheduleWithEDF(listOfTasks)
    else:
        raise ValueError("Unknown scheduling method inserted - must be one of FP, RM, or EDF")

    return processorUtilization

# plots the timing result
def plotResult(timingLists):
    pass

# main function handling whole structure
def main():
    listOfTasks, algMethod = getInputFromUser()
    processorUtilization = calProcessorUtilization(listOfTasks, algMethod)

    print(processorUtilization)
    #plotResult(timingLists)

######
# SIMPLE TEST:
# C_i = [2, 2, 5]
# T_i = [5, 9, 20]
# D_i = [3, 6, 5]
######

if __name__ == "__main__":
    main()
