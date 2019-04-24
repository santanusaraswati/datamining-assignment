# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 06:00:53 2019

@author: prasas
"""

# Load libraries
import pandas as pd
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation
from sklearn.metrics import confusion_matrix 
from sklearn.metrics import accuracy_score 
from sklearn.metrics import classification_report 
import statistics as stats

def loadData(filename):
    # load dataset
    rawdata = pd.read_csv(filename,header=None);
    
    dataset = pd.DataFrame(rawdata)
    rawY=dataset.iloc[:, 20]
    X=dataset.iloc[:, 0:19]
    
    #fix the class output Y
    f = lambda i : 0 if i == 0 else 1;
    Y = list(map(f, rawY));
    
    #fix the features
    for feature in X:
#        print(x[feature]);
        median = stats.median(X[feature]);
        print(median);
        X[feature] = list(map(lambda a: 1 if a >= median else 0, X[feature]))
    
    return X,Y


# Function to split the dataset 
def splitdataset(X,Y): 
 
    # Spliting the dataset into train and test 
    X_train, X_test, y_train, y_test = train_test_split(  
    X, Y, test_size = 0.3, random_state = 100); 
      
    return X_train, X_test, y_train, y_test 

# Function to perform training with giniIndex. 
def train_using_gini(X_train, X_test, y_train): 
  
    # Creating the classifier object 
    clf_gini = DecisionTreeClassifier(criterion = "gini", 
            random_state = 100,max_depth=3, min_samples_leaf=5) 
  
    # Performing training 
    clf_gini.fit(X_train, y_train) 
    return clf_gini 

# Function to perform training with entropy. 
def train_using_entropy(X_train, X_test, y_train): 
  
    # Decision tree with entropy 
    clf_entropy = DecisionTreeClassifier( 
            criterion = "entropy", random_state = 1)
  
    # Performing training 
    clf_entropy.fit(X_train, y_train) 
    return clf_entropy 

# Function to make predictions 
def prediction(X_test, clf_object): 
  
    # Predicton on test with giniIndex 
    y_pred = clf_object.predict(X_test) 
    print("Predicted values:") 
    print(y_pred) 
    return y_pred 
      
# Function to calculate accuracy 
def cal_accuracy(y_test, y_pred): 
     
    cmat = confusion_matrix(y_test, y_pred)
    a = cmat[1][1];
    b = cmat[0][1];
    c = cmat[1][0];
    d = cmat[0][0];
    
    accuracy = ((a+d)/(a+b+c+d))*100;
    fmeasure = ((2*a)/((2*a)+b+c)) * 100;
    #print("Confusion Matrix: ", cmat);
    
    return accuracy,fmeasure;
     
    

#main
def calcforfile(filename):
    X,Y = loadData(filename);
    X_train, X_test, y_train, y_test = splitdataset(X,Y);
    
    clf_entropy = train_using_entropy(X_train, X_test, y_train) 
    #print("Results Using Entropy:") 
    # Prediction using entropy 
    y_pred_entropy = prediction(X_test, clf_entropy) 
    accuracy,fmeasure = cal_accuracy(y_test, y_pred_entropy) 
    #print("F-measure", fmeasure);
    #print("accuracy", accuracy);
    return accuracy, fmeasure

#clf_gini = train_using_gini(X_train, X_test, y_train) 
#print("Results Using gini:") 
## Prediction using gini
#y_pred_gini = prediction(X_test, clf_gini) 
#cal_accuracy(y_test, y_pred_gini) 
    

import xlwt

def excelwrite(filename, sheet, list1, list2):
    book = xlwt.Workbook()
    sh = book.add_sheet(sheet)
    
    sh.write(0, 0, "File Number");
    sh.write(0, 1, "Accuracy");
    sh.write(0, 2, "F-Measure");
    
    
    row=1;

    for item in list1:
        sh.write(row, 1, item)
        sh.write(row, 0, str(row)+".csv")
        row = row+1;
    
    row=1;

    for item in list2:
        sh.write(row, 2, item)
        row=row+1;
        
    book.save(filename);
    print("file saved" + filename);
    return

accuracyList = list();
fmeasureList= list();

#for index in range(1,57):
accuracy,fmeasure = calcforfile("/home/santanu/study/mtech/semester2/Data Mining/data/1.csv");
#    accuracyList.append(accuracy);
#    fmeasureList.append(fmeasure);
print(accuracy)
print(fmeasure)
#excelwrite("d:\\2018HT12461_performance.xls", "AllData", accuracyList, fmeasureList);