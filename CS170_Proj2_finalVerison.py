#Name: Milind Devnani
#SID: 862134795
#NetID: mdevn001
#CS_170-Project2

import numpy as np
import sys
#import time

# We are using K = 1
# 1st column (col - 0) is label
print("Welcome to Milind Devnani's Feature Selection Algorithm:\n")
file = input("Type in the name of the file to test: \n")

# Read Data
#data = np.loadtxt(sys.argv[1])
data = np.loadtxt(file)
# get labels
labels = data[:,:1]
# get independent variables
variables = data[:,1:]
# count instances and features
(instances, features) = variables.shape

forwardOld = 0
backwardOld = 0
# Helper function to Standardize Data
def normalize_data():
    global variables
    # Calculate variable mean
    means = np.mean(variables, axis = 0)
    # Calculate variable standard deviation
    stds = np.std(variables, axis = 0)
    # Standardize data
    variables = np.reshape([(variables[i][j] - means[j])/stds[j] for i in range(instances) for j in range(features)], (instances, features))

    #for i in range (0,instances):
        #for j in range (0, features):
                    #print(variables[i, j])
    #print(np.sum(variables[:][1]))
#normalize_data()
#Parsed in values and normalized them/ testing conducted works!

# Helper function to calculate distance
def get_euclidean_distance(instance1, instance2):
    return sum([(instance1[i]-instance2[i])**2 for i in range(len(instance1))])**(1/2)
#print(get_euclidean_distance([2,4],[5,6]))

# Helper function to find first nearest neighbour of all data instances 
def get_neighbors(feature_list):
    data_set = variables[:,feature_list]
    # Helper function to find first nearest neighbour given index of the instance (data point)
    def get_neighbor(i):
        index = -1
        inst = data_set[i]
        dist = 1000000000
        for j in range(instances):
            if i != j:
                d = get_euclidean_distance(inst, data_set[j])
                if d < dist:
                    dist = d
                    index = j
        return (dist, labels[index][0])
    return [get_neighbor(i) for i in range(len(data_set))]

# Helper function to get accuracy of nearest neighbour estimator
def get_accuracy(feature_list):
    # Actual labels
    y = labels
    # predicted lables
    y_pred = [x[1] for x in get_neighbors(feature_list)]
    # Calculate Accuracy
    return (sum([y[i][0]==y_pred[i] for i in range(len(y))])+0.00)/len(y)    
#print(get_accuracy([0,1]))

#Implmented euclidean distance and nearest neighbors algorithm/ testing conducted works!

# Helper function for forward selection
def forwardIteration(currentFeatures, remainingFeatures):
    accuracy = 0
    global forwardOld
    if len(currentFeatures)>0:
        accuracy = get_accuracy(currentFeatures)
    current = currentFeatures.copy()
    for feature in remainingFeatures:
        #beginTimeSingleRun = time.time()
        c = currentFeatures.copy()
        r = remainingFeatures.copy()
        c.append(feature)
        r.remove(feature)
        acc = get_accuracy(c)
        #endTimeSingleRun = time.time()
        print("Using feature(s) ", [i+1 for i in c], ", accuracy is ", acc*100.0, "%") #, " Time Elasped: ", (endTimeSingleRun-beginTimeSingleRun), "seconds")
        if acc > accuracy:
            accuracy = acc
            current = c
    if accuracy != forwardOld:
        print("(Warning, Accuracy has decreased. Continuing search in case of local maxima) \n", "Feature subset ", [i+1 for i in current], "was best, accuracy is", accuracy*100, "%\n")
    forwardOld = accuracy
    print("Feature set ", [i+1 for i in current], " was best, accuracy is ", accuracy*100.0, "%")    
    return current, accuracy
#forwardIteration([i for i in range(features)], [])

def forward():
    #beginTime = time.time()
    accuracy = 0
    currentFeatures = []
    remainingFeatures = [i for i in range(features)]
    while len(remainingFeatures) > 0:
        cur, acc = forwardIteration(currentFeatures, remainingFeatures)
        if acc > accuracy:
            currentFeatures = cur.copy()
            accuracy = acc
            remainingFeatures = [i for i in range(features)]
            [remainingFeatures.remove(x) for x in cur]
        else:
            break
    #endTime = time.time()
    print("Forward Selection:")
    print("Finished search!! The best feature subset is ", [i+1 for i in currentFeatures], " which has an accuracy of ", accuracy*100.0, "%")#, " Total Time Elasped: ", (endTime-beginTime), "seconds")#finsished search
    return currentFeatures, accuracy

#forward()

#Implemented Forward selection/testing conducted works!

# Helper function for backward elimination
def backwardIteration(currentFeatures):
    accuracy = 0
    global backwardOld
    if len(currentFeatures)>0:
        accuracy = get_accuracy(currentFeatures)
    current = currentFeatures.copy()
    for feature in currentFeatures:
        #beginTimeSingleRun = time.time()
        c = currentFeatures.copy()
        c.remove(feature)
        acc = get_accuracy(c)
        #endTimeSingleRun = time.time()
        print("Using feature(s) ", [i+1 for i in c], ", accuracy is ", acc*100.0, "%") #, " Time Elasped: ", (endTimeSingleRun-beginTimeSingleRun), "seconds")
        if acc > accuracy:
            accuracy = acc
            current = c
    print("Feature set ", [i+1 for i in current], " was best, accuracy is ", accuracy*100.0, "%") 
    if accuracy != backwardOld:
        print("(Warning, Accuracy has decreased. Continuing search in case of local maxima) \n", "Feature subset ", [i+1 for i in current], "was best, accuracy is", accuracy*100, "%\n")
    backwardOld = accuracy   
    return current, accuracy
#backwardIteration([i for i in range(features)])

# Backward elimination seaarch
def backward():
    #beginTime = time.time()
    currentFeatures = [i for i in range(features)]
    #beginTimeSingleRun = time.time()
    accuracy = get_accuracy(currentFeatures)
    #endTimeSingleRun = time.time()
    print("Using feature(s) ", [i+1 for i in currentFeatures], ", accuracy is ", accuracy*100.0, "%") #, " Time Elasped: ", (endTimeSingleRun-beginTimeSingleRun), "seconds")
    while len(currentFeatures) > 0:
        cur, acc = backwardIteration(currentFeatures)
        if acc > accuracy:
            currentFeatures = cur.copy()
            accuracy = acc
        else:
            break
    #endTime = time.time()
    print("Backward Elimination:")
    print("Finished search!! The best feature subset is ", [i+1 for i in currentFeatures], " which has an accuracy of ", accuracy*100.0, "%") #, " Total Time Elasped: ", (endTime-beginTime), "seconds")#finished search
    return currentFeatures, accuracy

#backward()

def get_user_input():
    print("1: Forward Selection")
    print("2: Backward Elimination")
    searchType = input("Type the number of the feature selection method \n")
    return int(searchType)

def main():
    normalize_data()
    print("This dataset has ", features, " features (not including the class attribute), with", instances, " instances.\n")
    method = get_user_input()
    if method == 1:
        print("Running Forward Selection")
        forward()
    elif method == 2:
        print("Running Backward Elimination")
        backward()
    else:
        print("No Correct Method Selected")
        return

main()
#Completed Program: Backward elimination implemented/ testing conducted works!