#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 09:21:09 2018

@author: Cassidy
"""

'''Tutorial 8.4 – Hierarchial Clustering'''

import os
import importlib
import sys
import numpy as np
import pickle
from matplotlib import pyplot as plt


path = r'/Users/Cassidy/Documents/Assignments/F2018/M461/Algorithms'
if path not in sys.path:
    sys.path.append(path)
from ModuleDir import functions

dir(functions)

stateCodeDict = functions.stateCodeBuild()
fieldDict = functions.fieldDictBuild()

nameList = list(stateCodeDict.values())
noDataSet = set(nameList)

nIntervals = 30
intervals = [(12+2*i, 12+2*(i+1)) for i in range(nIntervals)]
histDict = {name:[0]*nIntervals for name in nameList}

n = 0
dataDict = {}
path = r'/Users/Cassidy/Documents/Assignments/F2018/M461/Algorithms/Data'
fileList = os.listdir(path)
for filename in fileList:
    try: 
        shortYear = int(filename[6:8])
        year = 2000 + shortYear
        fields = fieldDict[shortYear]
        sWt, eWt = fields['weight']
        sBMI, eBMI = fields['bmi']
        file = path + '//' + filename
        with open(file) as f:
            for record in f:
                # extract state codes
                stateCode = int(record[:2])
                stateName = stateCodeDict[stateCode]
                # extract BMI
                bmi = functions.convertBMI(record[sBMI-1:eBMI], shortYear)
                # extract sampling weight
                weight = float(record[sWt-1:eWt])
                # incrememnt sampling weight total for the intervals
                # containing bmi
                for i, interval in enumerate(intervals):
                    if interval[0]<bmi<=interval[1]:
                        histDict[stateName][i]+=weight
                        break
                noDataSet = noDataSet - set([stateName])
                n += 1
    except(ValueError):
        pass
    print(n)
    

print(len(histDict))
print(noDataSet)
for stateName in noDataSet:
    del histDict[stateName]
print(len(histDict))

for state in histDict:
    sumWeights = sum(histDict[state])
    histDict[state] = [intervalTotal/sumWeights for intervalTotal in histDict[state]]

    
# write histDict as pickle file
picklePath = '/Users/Cassidy/Documents/Assignments/F2018/M461/Algorithms/Data/histDict.pkl'
pickle.dump(histDict, open(picklePath, "wb"))

# initialize cluster dictionary
# key = cluster label state abbreviation
clusterDict = {state: [state] for state in histDict.keys()}

def mergeClusters(clusterDict, histDict):
    # extract keys from clusterDict
    stateList = list(clusterDict.keys())
    setList = [{a,b} for i, a in enumerate(stateList[:-1]) for b in stateList[i+1:]]
    
    # initialize minimum distance between clusters as 2
    mn = 2
    closestSet = {0,0}
    # iterate over setList and compute distance between associated
    # histograme. If distance < minimum distance, update min distance
    # and save set as closestSet. Print closestSet, which contains
    # labels of clusters to merge.
    for a, b in setList:
        abD = sum([abs(pai - pbi) for pai, pbi in zip(histDict[a], histDict[b])])
        if abD < mn:
            mn = abD
            closestSet = {a,b}
        print(closestSet, mn)
    
    # a, b are two closest clusters
    # replace relative proportions of cluster A with weighted average
    # of relative proportions from A and B
    a, b = closestSet
    na = len(clusterDict[a])
    nb = len(clusterDict[b])
    histDict[a] = [(na*pai + nb*pbi)/(na + nb) for pai, pbi in zip(histDict[a], histDict[b])]
    
    # extend member list of A with member list of B
    # remove B from the cluster dictionary
    clusterDict[a].extend(clusterDict[b])
    del clusterDict[b]
    return clusterDict, histDict
    
    # reduce initialset of 54 clusters to 5 clusters
while len(clusterDict) > 5:
    clusterDict, histDict = mergeClusters(clusterDict, histDict)
# print clusters and member states to counsole. 
for k, v in clusterDict.items():
    print(k, v)
        
# use pyplot to draw cluster histograms      
intervals = [(12+2*i,12+2*(i+1)) for i in range(30)]
x = [np.mean(pair) for pair in intervals][:19] # Ignore large BMI values.
for name in clusterDict:
    y = histDict[name][:19]
    plt.plot(x, y)
plt.legend([str(label) for label in range(6)], loc='upper right')
plt.legend(['CA', 'DC', 'HI', 'IA', 'MS'])
plt.xlabel('Body Mass Index')
plt.ylabel('Relative Frequency')
plt.title('Hierarchical clustering of states by BMI')
plt.grid(b=None, which='major', axis='both', linewidth='.25')
plt.show()

