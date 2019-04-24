# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 16:03:03 2019

@author: prasas
"""
import pandas as pd
import statistics as stats
import math as math
import xlwt

def loadData(filename):
    # load dataset
    rawdata = pd.read_csv(filename,header=None);

    dataset = pd.DataFrame(rawdata)
    rawY=dataset.iloc[:, 20]
    X=dataset.iloc[:, 0:20]

    #fix the class output Y
    f = lambda i : 1 if i > 0 else 0;
    Y = list(map(f, rawY));

    #fix the features
    for feature in X:
        #        print(x[feature]);
        median = stats.median(X[feature]);
        #print(median);
        X[feature] = list(map(lambda a: 1 if a >= median else 0, X[feature]))
    #print(X[0])
    #print(Y)
    return X,Y

def loadtestData(filename):
    # load dataset
    rawdata = pd.read_csv(filename,header=None);

    dataset = pd.DataFrame(rawdata)
    rawY=dataset.iloc[:, 2]
    X=dataset.iloc[:, 0:2]

    #fix the class output Y
    f = lambda i : 1 if i > 0 else 0;
    Y = list(map(f, rawY));

    #fix the features
    for feature in X:
        #        print(x[feature]);
        median = stats.median(X[feature]);
        #print(median);
        X[feature] = list(map(lambda a: 1 if a >= median else 0, X[feature]))

    return X,list(Y)


def getEntropy(vals):
    vallen = len(vals);

    if vallen == 0:
        return 0;

    count0 = vals.count(0);
    count1 = vals.count(1);


    F = lambda a: 0 if a <= 0 else -1*(a/vallen)*(math.log2(a/vallen))
    return F(count0) + F(count1);


def getGain(x,y):
    totalEntropy = getEntropy(y);
    #print(totalEntropy);
    gainList= list();
    for feature in x:
        bug0indices = [i for i, x in enumerate(x[feature]) if x == 0];
        bug0 = [y[i] for i in bug0indices];
        #print(bug0indices);
        #print(bug0);
        entropy0 = getEntropy(bug0);
        #print(entropy0)

        bug1indices = [i for i, x in enumerate(x[feature]) if x == 1];
        bug1 = [y[i] for i in bug1indices];
        entropy1 = getEntropy(bug1);
        #print(entropy1);

        tlen = len(x[feature]);
        gain = totalEntropy - ((len(bug0)/tlen)*entropy0) - ((len(bug1)/tlen)*entropy1);
        gainList.append(gain);

    return gainList;

def excelwrite(filename, gainlist):
    book = xlwt.Workbook()

    file=1;
    for item in gainlist:
        sh = book.add_sheet(str(file));
        column=0;
        for featuregain in item:
            #print(featuregain);
            sh.write(0, column, featuregain);
            column = column +1;
        file = file+1;
    book.save(filename);
    print("file saved" + filename);
    return

#x,y = loadData("data\\"+str(1)+".csv");
#gainlist = getGain(x,y);
#print(gainlist);
#allgainList = list();
#for i in range(1,57):
x,y = loadData("/home/santanu/study/mtech/semester2/Data Mining/data/1.csv")
print(getGain(x,y))
#    allgainList.append(gainlist);

#print(allgainList);
#excelwrite("d:\\2018HT12461_infogain.xls",allgainList);