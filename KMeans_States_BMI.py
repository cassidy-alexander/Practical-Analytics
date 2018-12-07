#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 09:40:36 2018

@author: Cassidy
"""

'''Tutorial 8.6 – the k-means algorithm'''

import numpy as np
import pickle
import matplotlib.pyplot as plt

picklePath = '/Users/Cassidy/Documents/Assignments/F2018/M461/Algorithms/Data/histDict.pkl'
histDict = pickle.load( open(picklePath, "rb" ) )
#print(len(histDict))

k=6
n = len(histDict)
# Randomize list of states
randomizedNames = np.random.choice(list(histDict.keys()), size = n, replace = False)

# Initialize ClusterDict Dictionary
clusterDict = {}
for i, state in enumerate(randomizedNames):
   clusterDict.setdefault(i%k,[]).append(state)
#print(clusterDict)

def clusterHistBuild(clusterDict, histDict):
    h = 30
    # create clusterHistDict to store to store k cluster histograms
    clusterHistDict = dict.fromkeys(clusterDict,[0]*h)
    for a in clusterDict:
        sumList = [0]*h  
        # iterate over states belonging to clusters    
        for state in clusterDict[a]:
            # use list comprehension to update sumList with data in histDict[state]  
            sumList = [(sumi + pmi) for sumi, pmi in zip(sumList, histDict[state])]
            na = len(clusterDict[a])
            # divide sums by number of states belonging to cluster
            clusterHistDict[a] = [sumi/na for sumi in sumList]
    return clusterHistDict

# build initial cluster centroids
clusterHistDict = clusterHistBuild(clusterDict, histDict)
#nearestCluster = 0
repeat = True
while repeat == True:
    # create dictionary to hold updated clusters
    updateDict = {}
    # Step 1
    # iterate over states
    for state in histDict:
        # initialize nearest distance
        mnD = 2
        stateHist = histDict[state]
        # find nearest cluster to a state and assign state to cluster
        for a in clusterDict:
            abD = sum([(pai-pbi)**2 for pai, pbi in zip(stateHist, clusterHistDict[a])])
            print('distance',abD)
            if abD<mnD:
                nearestCluster = a
                mnD = abD
        updateDict.setdefault(nearestCluster,[]).append(state)
    # Step 2
    # if clusterDict does not equal upDateDict, at least one state
    # has been assigned to a new cluster
    if clusterDict != updateDict:
        clusterDict = updateDict.copy()
        # update cluster dictionaries
        clusterHistDict = clusterHistBuild(clusterDict, histDict)
    else: 
        repeat = False
    #for a in updateDict:
        # print current assignments of states to clusters
        #print('Cluster =', a, ' Size = ', len(updateDict[a]), updateDict[a])
    

nIntervals = 30
intervals = [(12+2*i,12+2*(i+1)) for i in range(nIntervals)  ]
x = [np.mean(pair) for pair in intervals][:19]
for name in clusterDict:
    #print(name)
    y = clusterHistDict[name][:19]
    plt.plot(x, y)
plt.legend([str(label) for label in range(6)], loc='upper right')
plt.legend(['CA', 'DC', 'HI', 'IA', 'MS'])
plt.xlabel('Body Mass Index')
plt.ylabel('Relative Frequency')
plt.title('K-means clustering of states by BMI')
plt.grid(b=None, which='major', axis='both', linewidth='.25')
plt.show()
        
        