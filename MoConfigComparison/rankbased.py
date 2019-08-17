#!/usr/bin/python3
# coding=utf-8

"""
@desription: This file implements the rank-based method and geneartes the intermediate data
            1. generate divided data (train, validation and test sets) and save them into "prase_data/split_data/"
            2. use the rank-based method to obtain the sub_train set and save it into "parse_data/sub_train/"
            3. combines the validation set and the train set into "parse_data/combined_data/"
            4. combines the validation set and the sub_train set into "parse_data/combine_sub_train/"
----------------------------
@author: Yongfeng
@update: 2019.7.31
"""

import pandas as pd
import numpy as np
import os
from pandas import DataFrame
import random
from sklearn.utils import shuffle
from sklearn.tree import DecisionTreeRegressor
import warnings

class config:
    def __init__(self, id, decisions, objective, rank):
        self.id = id
        self.decision = decisions
        self.objective = objective
        self.rank = rank


class predicted_config:
    def __init__(self,decisions,objective,truly_rank,predicted,pre_rank):
        self.decision = decisions
        self.objective = objective
        self.truly_rank = truly_rank
        self.predicted = predicted
        self.pre_rank = pre_rank


def split_test_data(pdcontent, remain_test_ratios):
    """
    to divide the pdcontent into remaining set and test set by the ratio of remain_test_ratios
    """
    indepcolumns = pdcontent.columns[:-1]
    depcolumns = pdcontent.columns[-1]
    sorted_pdcontent = pdcontent.sort_values(depcolumns)  # sorted by performance

    content = []
    for c in range(len(pdcontent)):
        single_config = config(c, sorted_pdcontent.iloc[c][indepcolumns].tolist(), sorted_pdcontent.iloc[c][depcolumns], c)
        content.append(single_config)

    random.shuffle(content)
    len_content = len(content)
    index = int(remain_test_ratios[0]/sum(remain_test_ratios)*len_content)
 
    remain_set = content[:index]
    test_set = content[index:]  

    return [remain_set,test_set]  


def split_train_validation_data(remain_set, train_validation_ratios):
    """
    to divide the remain_set into training set and validation set by the ratio of train_validation_ratios
    """
    random.shuffle(remain_set)
    len_remain_set = len(remain_set)
    index = int(train_validation_ratios[0]/sum(train_validation_ratios)*len_remain_set)
 
    train_set = remain_set[:index]
    validation_set = remain_set[index:]  

    return [train_set, validation_set]  


def check_division_results(test_1, test_2):
    """
    We can use this to check the split function split_test_data and split_train_validation_data like this,
    ------------------------------------------
    check_division_results("E:\\git\\MoConfigComparison\\experiments\\rank_based\\rs-6d-c3-obj1\\rank_based0.csv",
                        "E:\\git\\MoConfigComparison\\experiments\\rank_based\\rs-6d-c3-obj1\\rank_based1.csv",)
    ------------------------------------------
    """
    pdcontent1 = pd.read_csv(test_1)
    configs1 = pdcontent1["Actual_Performance"]

    pdcontent2 = pd.read_csv(test_2)
    configs2 = pdcontent2["Actual_Performance"]

    flag = True
    for config in configs1:
        if config not in configs2:
            flag = False
            print(config)
            break
    if flag:
        print("[INFOR]: These two sets have the same configurations :)")
    else:
        print("[ERROR]: These two sets do not have the same configurations :(")

   
def split_data(pdcontent,fraction):
    """
    @deprecated: this function is never used
    """
    indepcolumns = pdcontent.columns[:-1]
    depcolumns = pdcontent.columns[-1]
    sorted_pdcontent = pdcontent.sort_values(depcolumns)  # sorted by performance

    content = []
    for c in range(len(pdcontent)):
        single_config = config(c, sorted_pdcontent.iloc[c][indepcolumns].tolist(), sorted_pdcontent.iloc[c][depcolumns], c)
        content.append(single_config)

    random.shuffle(content)
    indexes = range(len(content))
    len_content = len(pdcontent)

    indexes = [fraction[0], fraction[0]+fraction[1]]
 
    train_set = content[:int(indexes[0]*len_content)]
    validation_set = content[int(indexes[0]*len_content): int(indexes[1]*len_content)]
    test_set = content[int(indexes[1]*len_content):]  

    return [train_set,validation_set,test_set]


def update_data(data):
    x = [t.decision for t in data]
    y = [t.objective for t in data]
    data_x = DataFrame(x)
    data_x['Actual_Performance'] = DataFrame(y)
    
    return data_x


def rank_progressive(train, test):
    train_independent = [t.decision for t in train]
    train_dependent = [t.objective for t in train]

    sorted_test = sorted(test, key=lambda x: x.objective) # sorted by actual performance
    # for r,st in enumerate(sorted_test): st.rank = r
    test_independent = [t.decision for t in sorted_test]

    model = DecisionTreeRegressor()
    model.fit(train_independent, train_dependent)
    predicted = model.predict(test_independent)
    predicted_id = [[i,p] for i,p in enumerate(predicted)] 
    # bug  : shuffle before sorting
    # random.shuffle(predicted_id) # patch
    predicted_sorted = sorted(predicted_id, key=lambda x: x[-1]) # sorted by predicted performance
    predicted_rank_sorted = [[p[0], p[-1], i] for i,p in enumerate(predicted_sorted)]
    rank_diffs = [abs(p[0] - p[-1]) for p in predicted_rank_sorted]

    return np.mean(rank_diffs)


def wrapper_rank_progressive(train_set, validation_set):
    initial_size = 10
    training_indexes = range(len(train_set))
    shuffle(training_indexes)
    sub_train_set = [train_set[i] for i in training_indexes[:initial_size]] # randomly select 10 samples from train set
    steps = 0
    rank_diffs = []
    while (initial_size+steps) < len(train_set) - 1:
        rank_diffs.append(rank_progressive(sub_train_set, validation_set))
        policy_result = policy(rank_diffs)
        if policy_result != -1: break
        steps += 1
        sub_train_set.append(train_set[initial_size+steps])

    return sub_train_set


def policy(scores, lives=3):
    temp_lives = lives
    last = scores[0]
    for i,score in enumerate(scores):
        if i > 0:
            if temp_lives == 0:
                return i
            elif score >= last:
                temp_lives -= 1
                last = score
            else:
                temp_lives = lives
                last = score
    return -1


def predict_on_test(train, test):
    train_independent = [t.decision for t in train]
    train_dependent = [t.objective for t in train]

    sorted_test = sorted(test, key=lambda x: x.objective) # sorted by actual performance
    # for r, st in enumerate(sorted_test): st.rank = r
    test_independent = [t.decision for t in sorted_test]
    test_dependent = [t.objective for t in sorted_test]

    model = DecisionTreeRegressor()
    model.fit(train_independent, train_dependent)
    predicted = model.predict(test_independent)
    predicted_id = [[i, p] for i, p in enumerate(predicted)]

    # random.shuffle(predicted_id)  # patch: patch for the old version of the rank-based approach
    # predicted_sorted = sorted(predicted_id, key=lambda x: x[-1])
    # predicted_rank_sorted = [[p[0], p[-1], i] for i,p in enumerate(predicted_sorted)]
    # select_few = predicted_rank_sorted[:10]   # the min predicted rank
    
    test_content = list()
    for c in range(len(sorted_test)):
        test_config = predicted_config(test_independent[c], test_dependent[c], c+1, predicted[c], c+1)
        test_content.append(test_config)

    random.shuffle(test_content)  # patch: patch for the old version of the rank-based approach
    predicted_sorts = sorted(test_content,key = lambda x : x.predicted)
    for r, st in enumerate(predicted_sorts): st.pre_rank = r+1
    # select_few_modify = [t.truly_rank - 1 for t in predicted_sorts]
    
    return predicted_sorts


def find_min_actual_rank(predicted_sorts, top_K=10):  
    actual_ranks = [item.truly_rank for item in predicted_sorts[:top_K]]
    return min(actual_ranks)-1


def initialize_rank_based():
	# ignore the warning
    warnings.filterwarnings('ignore')
    pd.set_option('display.width',200)

    # parameter and path setting
    remain_test_ratios = [3,2] # remain:test = 3:2
    train_validation_ratios = [2,1] # train:validation = 2:1
    rounds = 50  # split rounds
    datafolder = "raw_data/"
    resultfolder = "experiments/rank_based/"
    trainfolder = "parse_data/sub_train/"
    splitfolder = "parse_data/split_data/"
            
    files = [datafolder + f for f in os.listdir(datafolder) if ".csv" in f]
    print(">> split and predict on test set using the rank-based method ...")
    for file in files:
        # print(file)
        filepath, full_filename = os.path.split(file)
        filename, ext = os.path.splitext(full_filename)
        print(filename)  

        pdcontent = pd.read_csv(file)
        if not os.path.exists(resultfolder + filename): # make directory in experiments/rank-based/
            os.makedirs(resultfolder + filename)
        if not os.path.exists(trainfolder + filename): # make directory in parse_data/sub_train/
            os.makedirs(trainfolder + filename)

        test_set, remain_set = split_test_data(pdcontent, remain_test_ratios) # split the data into remain and test set

        for i in range(rounds): # for each round
            if not os.path.exists(splitfolder + filename +'/split'+str(i)):
                os.makedirs(splitfolder + filename +'/split'+str(i))
            
            test = update_data(test_set)
            test.to_csv(splitfolder + filename +'/split'+str(i)+ '/test_set.csv', index=False) # test

            train_set, validation_set = split_train_validation_data(remain_set, train_validation_ratios) # split the data into train and validation set
            train = update_data(train_set)
            train.to_csv(splitfolder + filename +'/split'+str(i)+ '/train_set.csv', index=False) # train
            validation = update_data(validation_set)
            validation.to_csv(splitfolder + filename +'/split'+str(i)+ '/validation_set.csv', index=False) # validation
        #     data = pd.concat([train,validation],axis = 0)

        
            sub_train_set_rank = wrapper_rank_progressive(train_set, validation_set)
            sub_train = update_data(sub_train_set_rank)
            sub_train.to_csv(trainfolder + filename + '/rank_based'+str(i)+'.csv', index=False) # subtrain
            predicted_sorts = predict_on_test(sub_train_set_rank, test_set)
            
            test_data = DataFrame()
            test_data['Feature'] = [t.decision for t in predicted_sorts]
            test_data['Actual_Performance'] = [t.objective for t in predicted_sorts]
            test_data['Actual_Rank'] = [t.truly_rank for t in predicted_sorts]
            test_data['Predicted_Performance'] = [t.predicted for t in predicted_sorts]
            test_data['Predicted_Rank'] = [t.pre_rank for t in predicted_sorts]
                       
            test_data.to_csv(resultfolder + filename + '/rank_based'+str(i)+'.csv', index=False)


def combine_sub_train_and_validation():
    """
    this combined set is used for the rank based method: sub_train set + validation set
    """
    datafolder = "raw_data/"
    resultfolder = "parse_data/combined_sub_train/"
    trainfolder = "parse_data/sub_train/"
    splitfolder = "parse_data/split_data/"

    files = [datafolder + f for f in os.listdir(datafolder) if ".csv" in f]
    results = {}    
    rounds = 50  # split rounds
    print(">> combining the sub_train and validation sets ...")
    for file in files: # for each project
        # print(file)
        filepath, full_filename = os.path.split(file)
        filename, ext = os.path.splitext(full_filename)
        print(filename) # e.g., rs-6d-c3-obj1 
        if not os.path.exists(resultfolder + filename):
            os.makedirs(resultfolder + filename)
        for i in range(rounds): # for each round
            sub_train_path = trainfolder + filename + "/rank_based" + str(i) + ".csv"
            validation_path = splitfolder + filename + "/split" + str(i) + "/validation_set.csv"
            pdcontent_sub_train = pd.read_csv(sub_train_path)
            pdcontent_validation = pd.read_csv(validation_path)

            pdcontent = pd.concat([pdcontent_validation, pdcontent_sub_train])

            combine_train = resultfolder + filename + "/" + filename + "_" + str(i) + ".csv"
            pdcontent.to_csv(combine_train,index=False)


def combine_train_and_validation():
    """
    This combined set is used for MoConfig sampling method: train set and validation set
    """
    datafolder = "raw_data/"
    resultfolder = "parse_data/combined_train/"
    splitfolder = "parse_data/split_data/"

    files = [datafolder + f for f in os.listdir(datafolder) if ".csv" in f]
    results = {}    
    rounds = 50  # split rounds
    print(">> combining the train and validation sets ...")
    for file in files: # for each project
        # print(file)
        filepath, full_filename = os.path.split(file)
        filename, ext = os.path.splitext(full_filename)
        print(filename) # e.g., rs-6d-c3-obj1 
        if not os.path.exists(resultfolder + filename):
            os.makedirs(resultfolder + filename)
        for i in range(rounds): # for each round
            train_path = splitfolder + filename + "/split" + str(i) + "/validation_set.csv"
            validation_path = splitfolder + filename + "/split" + str(i) + "/validation_set.csv"
            pdcontent_train = pd.read_csv(train_path)
            pdcontent_validation = pd.read_csv(validation_path)

            pdcontent = pd.concat([pdcontent_validation, pdcontent_train])

            combine_train = resultfolder + filename + "/" + filename + "_" + str(i) + ".csv"
            pdcontent.to_csv(combine_train,index=False)


if __name__ == '__main__':
    # start of the rank-based method
    # initialize_rank_based()
    # combine_sub_train_and_validation()
    # combine_train_and_validation()

    
