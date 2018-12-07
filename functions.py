#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 09:08:54 2018

@author: Cassidy
"""

'''For each file, we need
    (a) position of body mass index
    (b) sampling weight
'''

def stateCodeBuild():
    path = r'/Users/Cassidy/Documents/Assignments/F2018/M461/national_county.txt'
    stateCodes = {}
    with open(path) as f: 
        for record in f:
            stateCode = int(record[3:5])
            stateCodes[stateCode] = record[0:2]
    return stateCodes



#Build the dictionary fieldDict
    #Keys = years
    #Values = bmi and weight positions
def fieldDictBuild():
    fieldDict = dict.fromkeys([0, 1, 2, 3, 11, 12, 13, 14])
    fieldDict[0] = {'bmi':(862, 864), 'weight':(832, 841), 'diabetes':85}
    fieldDict[1] = {'bmi':(725, 730), 'weight':(686, 695), 'diabetes':90}
    fieldDict[2] = {'bmi':(933, 936), 'weight':(822, 831), 'diabetes':100}
    fieldDict[3] = {'bmi':(854, 857), 'weight':(745, 754), 'diabetes':84}
    fieldDict[11] = {'genhlth':73, 'bmi':(1533, 1536), 'weight':(1475, 1484), 'income':(124, 125), 'education':122, 'diabetes':101}
    fieldDict[12] = {'genhlth':73, 'bmi':(1644, 1647), 'weight':(1449, 1458), 'income':(116, 117), 'education':114, 'diabetes':97}
    fieldDict[13] = {'genhlth':80, 'bmi':(2192, 2195), 'weight':(1953, 1962), 'income':(152, 153), 'education':150, 'diabetes':109}
    fieldDict[14] = {'genhlth':80, 'bmi':(2247, 2250), 'weight':(2007, 2016), 'income':(152, 153), 'education':150, 'diabetes':105}
    '''for year in fieldDict:
       print(year, fieldDict[year])'''
    return fieldDict


fieldDict = fieldDictBuild()



#Convert bmi to a floating point number
#floating point number:
    #computer approximation of the real number
def convertBMI(bmi, year):
    if year == 0 and bmi != '999':
        bmi = .1*float(bmi)
    elif year == 1 and bmi != '999999':
        bmi = .0001*float(bmi)
    elif 2 <= year <= 10 and bmi != '9999':
        bmi = .01*float(bmi)
    elif year > 10 and bmi != '    ': #blank string of length 4
        bmi = .01*float(bmi)
    else:
        bmi = 0
    return bmi

#save as function.py in ModuleDir folder
#bmi = convertBMI(bmi, year)

def getIncome(incomeString):
    #income is missing if the field consists of two blanks
    if incomeString != '  ':
        income = int(incomeString)
    else: 
        #we'll use the value 9 as a flag incicating that 
        #the record should be ignored
        income = 9
    return income

def getEducation(eduString):
    #education is missing if the field has one blank
    if eduString != ' ':
        education = int(eduString)
    else:
        #we'll use the value 9 as a flag indicating that the recoed
        #should be ignored
        education = 9
    return education


def getHlth(HlthString):
    #health is missing if the field has one blank
    if HlthString != ' ':
        genHlth = int(HlthString)
    else:
        #we'll use the value 9 as a flag indicating that the record
        #should be ignored
        genHlth = 9
    return genHlth

def getDiabetes(diabetesString):
    #health is missing if the field has one blank
    if diabetesString != ' ':
        diabetes = int(diabetesString)
    if diabetes in {2, 3, 4}:
        diabetes = 0
    if diabetes in {7, 9}:
        diabetes = -1
    else:
        #we'll use the value 9 as a flag indicating that the record
        #should be ignored
        diabetes = -1
    return diabetes
        


