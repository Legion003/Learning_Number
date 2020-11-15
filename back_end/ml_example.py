#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 21:59:00 2014

@author: Daifli

@school: Information Science.
"""

from numpy import *
import csv

def toInt(array):
    array=mat(array)
    m,n=shape(array)
    newArray=zeros((m,n))
    for i in xrange(m):
        for j in xrange(n):
                newArray[i,j]=int(array[i,j])
    return newArray
    
def nomalizing(array):
    m,n=shape(array)
    for i in xrange(m):
        for j in xrange(n):
            if array[i,j]!=0:
                array[i,j]=1
    return array
    
def loadTrainData():
    l=[]
    i=0
    with open('tmp_img_encode.txt') as file:
         lines=csv.reader(file)
         for line in lines:
             l.append(line) #42001*785
             i = i + 1
    l.remove(l[0])
    l=array(l)
    label=l[:,0]
    data=l[:,1:]
    print "norm all data."

    newArr = toInt(data)
    #print "TestOutput is: ",newArr[0]
    #print "Before toInt is: ", data[0]

    return nomalizing(toInt(data)),toInt(label)  #label 1*42000  data 42000*784
    #return trainData,trainLabel
    
def loadTestData():
    l=[]
    with open('test.csv') as file:
         lines=csv.reader(file)
         for line in lines:
             l.append(line)#28001*784
    l.remove(l[0])
    data=array(l)
    return nomalizing(toInt(data))  #  data 28000*784
    #return testData
    
def loadTestResult():
    l=[]
    with open('knn_benchmark.csv') as file:
         lines=csv.reader(file)
         for line in lines:
             l.append(line)#28001*2
    l.remove(l[0])
    label=array(l)
    return toInt(label[:,1])  #  label 28000*1
    
#result是结果列表 
#csvName是存放结果的csv文件名
def saveResult(result,csvName):
    with open(csvName,'wb') as myFile:    
        myWriter=csv.writer(myFile)
        for i in result:
            tmp=[]
            tmp.append(i)
            myWriter.writerow(tmp)
     
def saveJson(jstr, jpath):
    f=file(jpath, "w+")
    f.writelines(jstr)
    f.close()            

from sklearn.linear_model import LogisticRegression
def lrClassify(trainData, trainLabel, testData):
    lrClf=LogisticRegression(C=1000.0, random_state=0)
    lrClf.fit(trainData, trainLabel)
    testLabel=lrClf.predict(testData)
    return testLabel

import math
def cal_precision_recall_f1(y_test, result, cls_type):
    cor = 0
    err = 0
    all_cls = 0
    rmse = 0.00
    var = 0.00
    for i in range(0, y_test.size):
        rmse += float((y_test[i] - result[i]) ** 2)
        if ( result[i] == int(cls_type) ):
            all_cls += 1
            var += float(y_test[i] ** 2)
        if ( y_test[i] == int(cls_type) and result[i] == int(cls_type) ):
            cor += 1
        elif  ( y_test[i] == int(cls_type) and result[i] != int(cls_type) ):
            err += 1

    precision = float(cor)/float(all_cls)
    recall = float(cor)/float(cor+err)
    f1 = 2 * precision * recall / (precision + recall)
    vrmse = 1 - math.sqrt(rmse) / float(y_test.size)
    var = 1 - math.sqrt(var) / float(all_cls)
    return '%.2f' % precision,'%.2f' % recall,'%.2f' % f1, '%.2f' % vrmse, '%.2f' % var

from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
def digitRecognition():
    print "Begin Loading."
    trainData,trainLabel=loadTrainData()
    print "Finish Loading Training Data."
    #testData=loadTestData()
    #print len(trainData)
    #print len(trainLabel[0,:])
    X_train, X_test, Y_train, Y_test = train_test_split(trainData, trainLabel[0,:], test_size=0.3, random_state=0)
    print "Finish Loading Testing Data."
    #使用不同算法
    result50 = lrClassify(X_train, Y_train, X_test)
    
    #Evaluate The Results.
    target_names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    print (classification_report(Y_test, result50, target_names=target_names))

if __name__=='__main__':
    digitRecognition()
