import numpy as np
import matplotlib.pyplot as plt
from random import randint
import math

data = np.loadtxt("./mesh.dat", skiprows=1)
plt.plot(data[:,0], data[:,1], linewidth=0,marker='o',color='green', label='data')
#plt.xlabel("X")
#plt.ylabel("Y")
#plt.show()

def grahamscan(array):
    startingpoint = array[0]
    startingpointindex = 0
    for i in range(len(array)):
        if startingpoint[1] > array[i][1]:
            startingpoint = array[i]
            startingpointindex = i
        elif startingpoint[1] == array[i][1]:
            if startingpoint[0] > array[i][0]:
                startingpoint = array[i]
                startingpointindex = i
    sortedlist = []
    if startingpointindex==0:
        replacer = array[2]
        array[0] = replacer
        array[2] = startingpoint
        startingpointindex = 2
    elif startingpointindex == 1:
        replacer = array[3]
        array[1] = replacer
        array[3] = startingpoint
        startingpointindex = 3
    sortedlist.append(array[0])
    if (sortedlist[0][0]-startingpoint[0])*(array[1][1]-startingpoint[1]) - (sortedlist[0][1]-startingpoint[1])*(array[1][0]-startingpoint[0]) <= 0:
            sortedlist.insert(0,array[1])
    else:
        sortedlist.append(array[1])
    for i in range(2,len(array)):
        if array[i][0] != startingpoint[0] or array[i][1] != startingpoint[1]:
            lower = 0
            upper = len(sortedlist)-1
            if (sortedlist[lower][0]-startingpoint[0])*(array[i][1]-startingpoint[1]) - (sortedlist[lower][1]-startingpoint[1])*(array[i][0]-startingpoint[0]) <= 0:
                upper = 0
            elif (sortedlist[upper][0]-startingpoint[0])*(array[i][1]-startingpoint[1]) - (sortedlist[upper][1]-startingpoint[1])*(array[i][0]-startingpoint[0]) > 0:
                lower = len(sortedlist)
                upper = len(sortedlist)
            while (upper-lower > 1):
                midpoint = math.floor((lower+upper)/2)
                if (sortedlist[midpoint][0]-startingpoint[0])*(array[i][1]-startingpoint[1]) - (sortedlist[midpoint][1]-startingpoint[1])*(array[i][0]-startingpoint[0]) > 0:
                    lower = midpoint
                elif (sortedlist[midpoint][0]-startingpoint[0])*(array[i][1]-startingpoint[1]) - (sortedlist[midpoint][1]-startingpoint[1])*(array[i][0]-startingpoint[0]) < 0:
                    upper = midpoint
                else:
                    upper = midpoint
                    lower = midpoint
            if upper-lower == 1:
                lower = upper
            if upper >= len(sortedlist):
                sortedlist.append(array[i])
            else:
                sortedlist.insert(upper,array[i])
    
    
    finalist = [startingpoint, sortedlist[0], sortedlist[1]]
    for i in range(2,len(sortedlist)):
        while ((finalist[-1][0] - finalist[-2][0])*(sortedlist[i][1] - finalist[-1][1]) - (finalist[-1][1]-finalist[-2][1])*(sortedlist[i][0] - finalist[-1][0])) < 0:
            finalist.pop(-1)
        finalist.append(sortedlist[i])
    finalist.append(startingpoint)
    return finalist

def jarvismarch(array):
    basepoint = array[0]
    basepointindex = 0
    outputhull = []
    for i in range(len(array)):
        if array[i][0] < basepoint[0]:
            basepoint = array[i]
            basepointindex = i
        elif array[i][0] == basepoint[0]:
            if array[i][1] > basepoint[1]:
                basepoint = array[i]
                basepointindex=i
    originalbasepoint = array[basepointindex]
    outputhull.append(originalbasepoint)
    while (True):
        nextpoint = array[0]
        for i in range(1,len(array)):
            if array[i][0] != basepoint[0] or array[i][1] != basepoint[1]:
                if (nextpoint[0]-basepoint[0])*(array[i][1]-basepoint[1]) - (nextpoint[1]-basepoint[1])*(array[i][0]-basepoint[0]) >0:
                    nextpoint = array[i]
        basepoint = nextpoint
        if nextpoint[0] == originalbasepoint[0] and nextpoint[1] == originalbasepoint[1]:
            break
        else:
            outputhull.append(basepoint)
    outputhull.append(originalbasepoint)
    return outputhull

def monotonechain(array):
    sortedbyx = []
    if array[1][0] > array[0][0]:
        sortedbyx.append(array[0])
        sortedbyx.append(array[1])
    else:
        sortedbyx.append(array[1])
        sortedbyx.append(array[0])
    for i in range(2,len(array)):
        lower = 0
        upper = len(sortedbyx)-1
        if array[i][0] < sortedbyx[lower][0]:
            upper = 0
        elif array[i][0] > sortedbyx[upper][0]:
            lower = len(sortedbyx)
            upper = len(sortedbyx)
        while (upper - lower > 1):
            midpoint = math.floor((upper+lower)/2)
            if array[i][0] > sortedbyx[midpoint][0]:
                lower = midpoint
            elif array[i][0] < sortedbyx[midpoint][0]:
                upper = midpoint
            else:
                upper = midpoint
                lower = midpoint
        if upper-lower == 1:
            lower = upper
        if upper < len(sortedbyx):
            sortedbyx.insert(upper,array[i])
        else:
            sortedbyx.append(array[i])
        
    bottomhull = []
    for i in range(len(sortedbyx)):
        bottomhull.append(sortedbyx[i])
        if len(bottomhull)>2:
            while ((bottomhull[-1][0]-bottomhull[-3][0])*(bottomhull[-2][1]-bottomhull[-3][1]) - (bottomhull[-1][1]-bottomhull[-3][1])*(bottomhull[-2][0]-bottomhull[-3][0])>0):
                bottomhull.pop(-2)
                if len(bottomhull) < 3:
                    break
    tophull = []
    for i in range(len(sortedbyx)):
        tophull.append(sortedbyx[-1-i])
        if len(tophull)>2:
            while ((tophull[-1][0]-tophull[-3][0])*(tophull[-2][1]-tophull[-3][1]) - (tophull[-1][1]-tophull[-3][1])*(tophull[-2][0]-tophull[-3][0])>0):
                tophull.pop(-2)
                if len(tophull) < 3:
                    break
    for i in range(len(tophull)):
        bottomhull.append(tophull[i])
    return bottomhull

def xandy(array, offset):
    arrayx = []
    arrayy = []
    for i in range(len(array)):
        arrayx.append(array[i][0] + offset)
        arrayy.append(array[i][1])
    return arrayx, arrayy


grahamhullx, grahamhully = xandy(grahamscan(data),0)
jarvishullx, jarvishully = xandy(jarvismarch(data),0)
monotonehullx, monotonehully = xandy(monotonechain(data),0)

plt.plot(grahamhullx, grahamhully,color='red',label='graham scan hull')
plt.plot(jarvishullx, jarvishully,color='blue',label='jarvis march hull')
plt.plot(monotonehullx, monotonehully,color='black',label='monotone chain hull')
plt.xlabel("X")
plt.ylabel("Y")
plt.legend(loc = 'center')
plt.savefig("./plots/task1a")
plt.show