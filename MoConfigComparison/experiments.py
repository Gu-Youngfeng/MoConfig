#!/usr/bin/python3
# coding=utf-8

"""
@description: This file implements the experiments
			1. take the datasets in "parse_data/combined_data/" as the input of MoConfig "E:/git/MoConfigSampling/eclipse-workspace/testbed/input/"
			2. obtain results of MoCionfig "experiments/moconfig/"
----------------------------
@author: Yongfeng
@update: 2019.7.31
"""

import os
import pandas as pd
import re
import numpy as np

def search_raw_data(directory):
	
	files = [file for file in os.listdir(directory) if file.endswith(".csv")]
	# print(files)
	print("|%-25s|%-10s|%-10s|"%("Name","Features","Configs"))
	print("-------------------------------------------------")
	for file in files:
		get_basic_info(directory + file)


def get_basic_info(path):
	
	if not os.path.exists(path):
		print(">> ", path, " is not exist.")
		return None
	pdcontent = pd.read_csv(path)

	# print("|%-25s|%-10d|%-10d|"%(os.path.basename(path),len(pdcontent.columns)-1,len(pdcontent)))
	# print("%-25s&%-10d&%-10d\\\\"%(os.path.basename(path),len(pdcontent.columns)-1,len(pdcontent)))
	print("<tr><td class=\"name\">%-25s</td><td>%-10d</td><td>%-10d</td></tr>"%(os.path.basename(path),len(pdcontent.columns)-1,len(pdcontent)))


def to_numeric(line):

	line = line.strip()[1:-1] # remove the "[" and "]\n"

	if not ", " in line: # one point
		return [float(line)]
	else: # multiple points
		strs = line.split(", ")
		nums = [float(item) for item in strs]
		return nums


def read_eclipse_results(path):
	file = open(path)
	lines = file.readlines()
	datas = []
	data = []
	projs = []
	flag= False
	for line in lines:
		if line.startswith("### ") and flag is False:
			flag = True
			projs.append(line.strip()[4:])
			# print(">", line)
		elif line.startswith("### ") and flag is True:
			datas.append(data)
			data = []
			projs.append(line.strip()[4:])
			# print(">>", line)
		elif line.startswith("[") and flag is True:
			data_line = to_numeric(line)
			data.append(data_line)
	# print(projs)
	datas.append(data)
	return [projs, datas]


def draw_multi_obj(proj, data):

	import matplotlib.pyplot as plt
	import matplotlib.ticker as ticker
	plt.figure(figsize=(15,4))

	plt.subplot(131) # NUMSAMPLE & ENTROPY
	x_00 = [int(i) for i in data[0]]
	y_00 = data[1] # NSGA-II
	# x_01 = data[2]
	# y_01 = data[3] # DBEA
	# x_02 = data[4]
	# y_02 = data[5] # eMOEA
	# x_03 = data[6]
	# y_03 = data[7] # IBEA
	ax1 = plt.scatter(x_00, y_00, marker="^", color="orange")
	# plt.scatter(x_01, y_01, marker="^")
	# plt.scatter(x_02, y_02, marker="X")
	# plt.scatter(x_03, y_03, marker="2")
	# plt.gca().ticklabel_format(useOffset=False, style='plain')
	plt.gca().xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
	plt.xlim([126,140])
	# plt.ylim([9990, 10000])
	plt.ylabel("entropy", fontsize=15) 
	plt.xlabel("cost", fontsize=15)
	# plt.legend(["NSGA-II","DBEA","eMOEA","IBEA"])

	plt.subplot(132) # NUMSAMPLE & VARIANCE
	x_10 = [int(i) for i in data[8]]
	y_10 = data[9] # NSGA-II
	# x_11 = data[10]
	# y_11 = data[11] # DBEA
	# x_12 = data[12]
	# y_12 = data[13] # eMOEA
	# x_13 = data[14]
	# y_13 = data[15] # IBEA
	plt.scatter(x_10, y_10, marker="+", color="green")
	# plt.scatter(x_11, y_11, marker="^")
	# plt.scatter(x_12, y_12, marker="X")
	# plt.scatter(x_13, y_13, marker="2")
	# plt.gca().ticklabel_format(useOffset=False, style='plain')
	plt.gca().xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
	plt.xlim([300,650])
	# plt.ylim([9980, 10000])
	plt.ylabel("variance", fontsize=15) 
	plt.xlabel("cost", fontsize=15)
	# plt.legend(["NSGA-II","DBEA","eMOEA","IBEA"])

	plt.subplot(133) # NUMSAMPLE & DENSITY
	x_20 = [int(i) for i in data[16]]
	y_20 = data[17] # NSGA-II
	# x_21 = data[18]
	# y_21 = data[19] # DBEA
	# x_22 = data[20]
	# y_22 = data[21] # eMOEA
	# x_23 = data[22]
	# y_23 = data[23] # IBEA
	plt.scatter(x_20, y_20, marker="2", color="red")
	# plt.scatter(x_21, y_21, marker="^")
	# plt.scatter(x_22, y_22, marker="X")
	# plt.scatter(x_23, y_23, marker="2")
	# plt.gca().ticklabel_format(useOffset=False, style='plain')
	plt.gca().xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
	plt.xlim([90, 95])
	# plt.ylim([9980, 10000])
	plt.ylabel("density", fontsize=15) 
	plt.xlabel("cost", fontsize=15)
	# plt.legend(["NSGA-II","DBEA","eMOEA","IBEA"])
	# plt.text(0.5, 0.5, "Non-dominated solutions in " + proj)
	plt.tight_layout()

	# plt.subplots_adjust(wspace=0.2, bottom=0.32)
	plt.savefig("pics/solutions/"+proj+".jpg")
	plt.show()


def draw_combine_train(data):
	projs = ['rs-6d-c3-obj1', 'rs-6d-c3-obj2', 'snw', 'sol-6d-c2-obj1', 'sol-6d-c2-obj2', 'wc+rs-3d-c4-obj1', 'wc+rs-3d-c4-obj2', 'wc+sol-3d-c4-obj1', 'wc+sol-3d-c4-obj2', 'wc+wc-3d-c4-obj1', 'wc+wc-3d-c4-obj2', 'wc-3d-c4-obj1', 'wc-3d-c4-obj2', 'wc-5d-c5-obj1', 'wc-5d-c5-obj2', 'wc-6d-c1-obj1', 'wc-6d-c1-obj2', 'wc-c1-3d-c1-obj1', 'wc-c1-3d-c1-obj2', 'wc-c3-3d-c1-obj1', 'wc-c3-3d-c1-obj2']
	# data = [550.74, 554.94, 53.14, 405.4, 409.26, 52.3, 49.7, 50.66, 53.4, 49.22, 48.6, 134.04, 129.96, 172.08, 178.34, 419.94, 429.44, 217.96, 212.32, 231.3, 235.98]

	x = range(len(data))
	import matplotlib.pyplot as plt
	plt.figure(figsize=(10,5))

	plt.bar(x, data)
	plt.title("the required measurement cost (sub_train + validation) using the rank based approach")
	plt.xlabel("projects")
	plt.ylabel("number of configurations")

	plt.savefig("pics/rankBasedCost.jpg")
	plt.show()


def draw_rank_based_minRD(data):
	projs = ['rs-6d-c3-obj1', 'rs-6d-c3-obj2', 'snw', 'sol-6d-c2-obj1', 'sol-6d-c2-obj2', 'wc+rs-3d-c4-obj1', 'wc+rs-3d-c4-obj2', 'wc+sol-3d-c4-obj1', 'wc+sol-3d-c4-obj2', 'wc+wc-3d-c4-obj1', 'wc+wc-3d-c4-obj2', 'wc-3d-c4-obj1', 'wc-3d-c4-obj2', 'wc-5d-c5-obj1', 'wc-5d-c5-obj2', 'wc-6d-c1-obj1', 'wc-6d-c1-obj2', 'wc-c1-3d-c1-obj1', 'wc-c1-3d-c1-obj2', 'wc-c3-3d-c1-obj1', 'wc-c3-3d-c1-obj2']
	# data = [32.799999999999997, 50.759999999999998, 2.3599999999999999, 43.799999999999997, 25.120000000000001, 3.46, 1.4199999999999999, 3.7799999999999998, 1.48, 7.4000000000000004, 2.02, 9.0199999999999996, 8.2599999999999998, 24.0, 9.2799999999999994, 37.340000000000003, 21.219999999999999, 12.94, 25.780000000000001, 29.899999999999999, 17.34]

	x = range(len(data))
	import matplotlib.pyplot as plt
	plt.figure(figsize=(10,5))

	plt.bar(x, data)
	plt.title("the minRDs using the rank based approach")
	plt.xlabel("projects")
	plt.ylabel("minRDs")

	plt.savefig("pics/rankBasedRD.jpg")
	plt.show()


def draw_rank_based_mmre(data):
	projs = ['rs-6d-c3-obj1', 'rs-6d-c3-obj2', 'snw', 'sol-6d-c2-obj1', 'sol-6d-c2-obj2', 'wc+rs-3d-c4-obj1', 'wc+rs-3d-c4-obj2', 'wc+sol-3d-c4-obj1', 'wc+sol-3d-c4-obj2', 'wc+wc-3d-c4-obj1', 'wc+wc-3d-c4-obj2', 'wc-3d-c4-obj1', 'wc-3d-c4-obj2', 'wc-5d-c5-obj1', 'wc-5d-c5-obj2', 'wc-6d-c1-obj1', 'wc-6d-c1-obj2', 'wc-c1-3d-c1-obj1', 'wc-c1-3d-c1-obj2', 'wc-c3-3d-c1-obj1', 'wc-c3-3d-c1-obj2']
	# data = [32.799999999999997, 50.759999999999998, 2.3599999999999999, 43.799999999999997, 25.120000000000001, 3.46, 1.4199999999999999, 3.7799999999999998, 1.48, 7.4000000000000004, 2.02, 9.0199999999999996, 8.2599999999999998, 24.0, 9.2799999999999994, 37.340000000000003, 21.219999999999999, 12.94, 25.780000000000001, 29.899999999999999, 17.34]

	x = range(len(data))
	import matplotlib.pyplot as plt
	plt.figure(figsize=(10,5))

	plt.plot(x, data)
	plt.title("the MMRE using the rank based approach")
	plt.xlabel("projects")
	plt.ylabel("MMRE")
	plt.yscale("log")

	plt.savefig("pics/rankBasedMMRE.jpg")
	plt.show()
	

def get_combined_sub_train_size(proj):
    splitfolder = "parse_data/combined_sub_train/"
    rounds = 50
    sizes = []

    for i in range(rounds):
    	file_name = splitfolder + proj + "/" + proj + "_" + str(i) + ".csv"
    	# print(file_name)
    	pdcontent = pd.read_csv(file_name)
    	sizes.append(len(pdcontent))
    
    sumS = 0
    for size in sizes:
    	sumS += size
    # print(sizes)
    return sumS/len(sizes) 


def get_whole_combined_sub_train_size():

    datafolder = "raw_data/"           
    files = [f[:-4] for f in os.listdir(datafolder) if ".csv" in f]
    # print(files)

    combine_train_sizes = []
    for file in files:
    	mean_size = get_combined_sub_train_size(file)
    	combine_train_sizes.append(mean_size)

    return combine_train_sizes


def get_minRD(proj, topK):
    resultfolder = "experiments/rank_based/"
    rounds = 50
    minRD = []

    for i in range(rounds):
    	file_name = resultfolder + proj + "/rank_based" + str(i) + ".csv"
    	pdcontent = pd.read_csv(file_name)
    	actual_ranks = pdcontent["Actual_Rank"]
    	minRD.append(min(actual_ranks[:topK]))

    sumRD = 0
    for rd in minRD:
    	sumRD += rd
    return sumRD/len(minRD) 


def get_whole_minRD(topK=10):
    datafolder = "raw_data/"           
    files = [f[:-4] for f in os.listdir(datafolder) if ".csv" in f]
    # print(files)

    minRDs = []
    for file in files:
    	minRD = get_minRD(file, topK)
    	minRDs.append(minRD)

    return minRDs


def get_mmre(proj):
    resultfolder = "experiments/rank_based/"
    rounds = 50
    mmres = []

    for i in range(rounds):
    	file_name = resultfolder + proj + "/rank_based" + str(i) + ".csv"
    	pdcontent = pd.read_csv(file_name)
    	actual_performances = pdcontent["Actual_Performance"]
    	predicted_performances = pdcontent["Predicted_Performance"]

    	deltas = []
    	for act, pre in zip(actual_performances, predicted_performances):
    		delta = abs(act - pre)/act
    		deltas.append(delta)   	
    	sumD = 0
    	for delta in deltas:
    		sumD += delta
    	mmres.append(sumD/len(deltas))

    sumM = 0
    for mmre in mmres:
    	sumM += mmre

    return sumM/len(mmres)


def get_whole_mmre():
    datafolder = "raw_data/"           
    files = [f[:-4] for f in os.listdir(datafolder) if ".csv" in f]
    # print(files)

    mmres = []
    for file in files:
    	mean_mmre = get_mmre(file)
    	mmres.append(mean_mmre)

    return mmres


def compare_rank_based_with_moconfig(proj, ga_method):
	rankbased_root = "experiments/rank_based/" + proj
	rankbased_cost = "parse_data/combined_sub_train/" + proj
	moconfig_root = "experiments/moconfig/" + proj + "/" + ga_method

	# obtain the results of the rank-based method
	rounds = 50
	rankbased_minRD = []
	rankbased_samples = []
	for i in range(rounds):
		file_name = rankbased_root + "/rank_based" + str(i) + ".csv"
		pdcontent = pd.read_csv(file_name)
		actual_ranks = pdcontent["Actual_Rank"]
		rankbased_minRD.append(min(actual_ranks[:10]))

		file_name_2 = rankbased_cost + "/" + proj + "_" + str(i) + ".csv"
		pdcontent = pd.read_csv(file_name_2)
		rankbased_samples.append(len(pdcontent))

	# print(rankbased_samples)
	# print(rankbased_minRD)

	# obtain the results of the MoConfig, 1: NUMSAMPLE_ENTROPY, 2: NUMSAMPLE_VARIANCE, 3: NUMSAMPLE_DENSITY
	##### 1: NUMSAMPLE_ENTROPY
	moconfig1_minRD = []
	moconfig1_samples = [] 
	results1_files = [f for f in os.listdir(moconfig_root + "/NUMSAMPLE_ENTROPY") if f.endswith(".csv")]
	for results in results1_files:
		file_name = moconfig_root + "/NUMSAMPLE_ENTROPY/" + results
		pdcontent = pd.read_csv(file_name)
		actual_ranks = pdcontent["Actual_Rank"]
		moconfig1_minRD.append(min(actual_ranks[:10]))

		pattern = "moconfig_(.*).csv"
		matchObj = re.match(pattern, results)
		samples = ""
		if matchObj:
			samples = matchObj.group(1)
			# print(samples)
			ft_samples = float(samples)
			moconfig1_samples.append(ft_samples)

	##### 2: NUMSAMPLE_VARIANCE
	moconfig2_minRD = []
	moconfig2_samples = [] 
	results2_files = [f for f in os.listdir(moconfig_root + "/NUMSAMPLE_VARIANCE") if f.endswith(".csv")]
	for results in results2_files:
		file_name = moconfig_root + "/NUMSAMPLE_VARIANCE/" + results
		pdcontent = pd.read_csv(file_name)
		actual_ranks = pdcontent["Actual_Rank"]
		moconfig2_minRD.append(min(actual_ranks[:10]))

		pattern = "moconfig_(.*).csv"
		matchObj = re.match(pattern, results)
		samples = ""
		if matchObj:
			samples = matchObj.group(1)
			# print(samples)
			ft_samples = float(samples)
			moconfig2_samples.append(ft_samples)

	# print(moconfig2_samples)
	# print(moconfig2_minRD)

	##### 3: NUMSAMPLE_DENSITY
	moconfig3_minRD = []
	moconfig3_samples = [] 
	results3_files = [f for f in os.listdir(moconfig_root + "/NUMSAMPLE_DENSITY") if f.endswith(".csv")]
	for results in results3_files:
		file_name = moconfig_root + "/NUMSAMPLE_DENSITY/" + results
		pdcontent = pd.read_csv(file_name)
		actual_ranks = pdcontent["Actual_Rank"]
		moconfig3_minRD.append(min(actual_ranks[:10]))

		pattern = "moconfig_(.*).csv"
		matchObj = re.match(pattern, results)
		samples = ""
		if matchObj:
			samples = matchObj.group(1)
			# print(samples)
			ft_samples = float(samples)
			moconfig3_samples.append(ft_samples)

	# print(moconfig3_samples)
	# print(moconfig3_minRD)
	return [rankbased_samples, rankbased_minRD, 
			moconfig1_samples, moconfig1_minRD, 
			moconfig2_samples, moconfig2_minRD,
			moconfig3_samples, moconfig3_minRD]


def draw_comparision_minRD(proj, ga_method):

	datas = compare_rank_based_with_moconfig(proj, ga_method)

	import matplotlib.pyplot as plt
	plt.figure(figsize=(5,4))

	# rankbased_samples = [261, 220, 221, 222, 230, 216, 256, 237, 221, 269, 249, 229, 219, 249, 234, 237, 249, 216, 249, 257, 225, 255, 218, 220, 228, 306, 232, 235, 227, 234, 234, 223, 245, 216, 220, 227, 234, 233, 219, 232, 241, 246, 277, 238, 220, 237, 219, 238, 219, 260]	
	# rankbased_minRDs = [2, 41, 1, 46, 5, 50, 2, 93, 5, 4, 4, 45, 4, 2, 43, 9, 17, 2, 4, 1, 14, 23, 34, 5, 13, 2, 2, 1, 28, 1, 16, 28, 3, 122, 11, 1, 7, 10, 49, 2, 4, 4, 3, 35, 2, 4, 15, 6, 36, 6]
	rankbased_samples = datas[0]
	rankbased_minRDs = datas[1]
	plt.scatter(rankbased_samples, rankbased_minRDs, marker=".")

	# moconfig1_samples = [135.0, 136.0, 138.0, 140.0, 145.0, 147.0, 149.0, 151.0, 152.0]
	# moconfig1_minRDs = [48, 11, 54, 18, 5, 2, 23, 11, 12]
	moconfig1_samples = datas[2]
	moconfig1_minRDs = datas[3]
	plt.scatter(moconfig1_samples, moconfig1_minRDs, marker="^")

	# moconfig2_samples = [329.0, 338.0, 340.0, 343.0, 345.0, 347.0, 349.0, 353.0, 355.0, 358.0, 361.0, 363.0, 364.0, 367.0, 371.0, 372.0, 373.0, 380.0, 382.0, 388.0, 389.0, 391.0, 393.0, 395.0, 398.0, 399.0, 402.0, 404.0, 407.0, 410.0, 412.0, 413.0, 417.0, 419.0, 420.0, 421.0, 423.0, 426.0, 428.0, 431.0, 433.0, 436.0, 439.0, 441.0, 445.0, 449.0, 450.0, 452.0, 455.0, 456.0, 458.0, 460.0, 461.0, 464.0, 467.0, 468.0, 470.0, 472.0, 479.0, 480.0, 485.0, 487.0, 489.0, 492.0, 497.0, 499.0, 502.0, 508.0, 509.0, 512.0, 517.0, 522.0, 524.0, 525.0, 529.0, 531.0, 535.0, 543.0, 545.0, 547.0, 550.0, 554.0, 557.0, 561.0, 563.0, 565.0, 567.0, 568.0, 572.0, 574.0, 576.0, 580.0, 581.0, 584.0, 586.0, 590.0, 594.0, 596.0, 597.0, 605.0]
	# moconfig2_minRDs = [11, 11, 7, 13, 42, 11, 8, 11, 11, 12, 12, 33, 11, 11, 11, 12, 9, 11, 11, 13, 12, 11, 15, 12, 13, 28, 7, 11, 13, 11, 12, 11, 11, 13, 62, 11, 12, 12, 13, 12, 12, 11, 12, 42, 11, 26, 11, 11, 13, 12, 11, 12, 13, 13, 29, 10, 11, 10, 12, 8, 11, 11, 1, 1, 11, 13, 11, 13, 49, 11, 13, 70, 8, 21, 13, 11, 12, 12, 25, 13, 11, 12, 8, 12, 12, 13, 9, 11, 8, 12, 11, 11, 11, 9, 11, 8, 13, 13, 12, 13]
	moconfig2_samples = datas[4]
	moconfig2_minRDs = datas[5]
	plt.scatter(moconfig2_samples, moconfig2_minRDs, marker="+")

	# moconfig3_samples = [103.0, 94.0]
	# moconfig3_minRDs = [11, 14]
	moconfig3_samples = datas[6]
	moconfig3_minRDs = datas[7]
	plt.scatter(moconfig3_samples, moconfig3_minRDs, marker="2")

	plt.xlabel("cost", fontsize=15)
	plt.ylabel("accuracy - RD(10)", fontsize=15)
	plt.yscale("log") #### y = log(y)
	# plt.ylim([0.8, 50])
	plt.xlim([0, 650])
	# plt.title("Predicted minRD of " + proj + " using the " + ga_method)
	plt.legend(["rank-based", "entropy-cost", "variance-cost", "density-cost"],
		# loc='upper center', bbox_to_anchor=(-0.6,0.95),ncol=3,fancybox=True,shadow=True
		)

	plt.subplots_adjust(wspace=0.2)
	savefile = "pics/algorithms/" + proj + "_" + ga_method + ".jpg"
	plt.savefig(savefile)
	plt.show()


def table_comparision_minRD(proj, ga_method):

	datas = compare_rank_based_with_moconfig(proj, ga_method)
	
	# rankp-based method 
	rankbased_samples = datas[0]
	rankbased_minRDs = datas[1]
	rankbased_solution = len(rankbased_samples)
	rankbased_ave_minRD = np.mean(rankbased_minRDs)
	rankbased_ave_samples = np.mean(rankbased_samples)
	
	# combination: entropy-cost 
	moconfig1_samples = datas[2]
	moconfig1_minRDs = datas[3]
	moconfig1_solution = len(moconfig1_samples)
	moconfig1_ave_minRD = np.mean(moconfig1_minRDs)
	moconfig1_ave_samples = np.mean(moconfig1_samples)
	
	# combintion: variance-cost
	moconfig2_samples = datas[4]
	moconfig2_minRDs = datas[5]
	moconfig2_solution = len(moconfig2_samples)
	moconfig2_ave_minRD = np.mean(moconfig2_minRDs)
	moconfig2_ave_samples = np.mean(moconfig2_samples)
	
	# combination: density-cost
	moconfig3_samples = datas[6]
	moconfig3_minRDs = datas[7]
	moconfig3_solution = len(moconfig3_samples)
	moconfig3_ave_minRD = np.mean(moconfig3_minRDs)
	moconfig3_ave_samples = np.mean(moconfig3_samples)

	print("<tr><td class=\"name\"> %-18s </td><td> %d </td><td> %.2f </td><td> %.2f </td><td> %d </td><td> %.2f </td><td> %.2f </td><td> %d </td><td> %.2f </td><td> %.2f </td><td> %d </td><td> %.2f </td><td> %.2f </td></tr>"%
		(proj, rankbased_solution, rankbased_ave_samples, rankbased_ave_minRD, 
			   moconfig1_solution, moconfig1_ave_samples, moconfig1_ave_minRD,
			   moconfig2_solution, moconfig2_ave_samples, moconfig2_ave_minRD,
			   moconfig3_solution, moconfig3_ave_samples, moconfig3_ave_minRD))


def get_time_cost():

	projs = ['rs-6d-c3-obj1', 'rs-6d-c3-obj2', 'snw', 'sol-6d-c2-obj1', 'sol-6d-c2-obj2', 'wc+rs-3d-c4-obj1', 'wc+rs-3d-c4-obj2', 'wc+sol-3d-c4-obj1', 'wc+sol-3d-c4-obj2', 'wc+wc-3d-c4-obj1', 'wc+wc-3d-c4-obj2', 'wc-3d-c4-obj1', 'wc-3d-c4-obj2', 'wc-5d-c5-obj1', 'wc-5d-c5-obj2', 'wc-6d-c1-obj1', 'wc-6d-c1-obj2', 'wc-c1-3d-c1-obj1', 'wc-c1-3d-c1-obj2', 'wc-c3-3d-c1-obj1', 'wc-c3-3d-c1-obj2']
	data_1 = [1143.2,1103.1,131.4,764.2,742.5,90.6,105.3,89.2,93.8,116.2,96.9,263.6,242.4,231.8,241.1,758.1,766.2,417.5,390.8,450.0,443.7]
	data_2 = [2133.1,1647.1,242.0,1536.8,1311.7,271.7,231.9,240.2,197.1,204.8,178.3,807.7,743.5,911.9,1258.0,1650.5,1474.0,803.1,839.5,811.7,798.6]
	data_3 = [720.5,701.7,47.2,477.6,461.1,44.1,46.3,43.0,43.0,48.2,41.7,89.8,83.3,135.8,140.4,474.3,473.3,158.0,154.6,185.9,175.0]

	for i in range(len(projs)):
		print(projs[i], "&", data_1[i], "&", data_2[i], "&", data_3[i], "\\\\")

	for i in range(len(projs)):
		print("<tr><td class=\"name\">", projs[i], "</td><td>", data_1[i], "</td><td>", data_2[i], "</td><td>", data_3[i], "</td></tr>")

	print(np.mean(data_1), np.mean(data_2), np.mean(data_3))


def draw_combination_3_1(proj, data, ga_method):
	import matplotlib.pyplot as plt
	import matplotlib.ticker as ticker
	plt.figure(figsize=(18,3.8))

	######################  THREE PLOTS

	plt.subplot(141) # NUMSAMPLE & ENTROPY
	x_00 = [int(i) for i in data[0]]
	y_00 = data[1] # NSGA-II
	ax1 = plt.scatter(x_00, y_00, marker="^", color="orange")
	# plt.gca().ticklabel_format(useOffset=False, style='plain')
	plt.gca().xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
	# plt.xlim([126,140])
	# plt.ylim([9990, 10000])
	plt.ylabel("entropy", fontsize=15) 
	plt.xlabel("cost", fontsize=15)
	# plt.legend(["NSGA-II","DBEA","eMOEA","IBEA"])

	plt.subplot(142) # NUMSAMPLE & VARIANCE
	x_10 = [int(i) for i in data[8]]
	y_10 = data[9] # NSGA-II
	plt.scatter(x_10, y_10, marker="+", color="green")
	# plt.gca().ticklabel_format(useOffset=False, style='plain')
	plt.gca().xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
	# plt.xlim([300,650])
	# plt.ylim([9980, 10000])
	plt.ylabel("variance", fontsize=15) 
	plt.xlabel("cost", fontsize=15)
	# plt.legend(["NSGA-II","DBEA","eMOEA","IBEA"])

	plt.subplot(143) # NUMSAMPLE & DENSITY
	x_20 = [int(i) for i in data[16]]
	y_20 = data[17] # NSGA-II
	plt.scatter(x_20, y_20, marker="2", color="red")
	# plt.gca().ticklabel_format(useOffset=False, style='plain')
	plt.gca().xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
	# plt.xlim([90, 95])
	# plt.ylim([9980, 10000])
	plt.ylabel("density", fontsize=15) 
	plt.xlabel("cost", fontsize=15)
	# plt.legend(["NSGA-II","DBEA","eMOEA","IBEA"])
	# plt.text(0.5, 0.5, "Non-dominated solutions in " + proj)


	################  SCATER PLOT
	
	datas = compare_rank_based_with_moconfig(proj, ga_method)
	# rankbased_samples = [261, 220, 221, 222, 230, 216, 256, 237, 221, 269, 249, 229, 219, 249, 234, 237, 249, 216, 249, 257, 225, 255, 218, 220, 228, 306, 232, 235, 227, 234, 234, 223, 245, 216, 220, 227, 234, 233, 219, 232, 241, 246, 277, 238, 220, 237, 219, 238, 219, 260]	
	# rankbased_minRDs = [2, 41, 1, 46, 5, 50, 2, 93, 5, 4, 4, 45, 4, 2, 43, 9, 17, 2, 4, 1, 14, 23, 34, 5, 13, 2, 2, 1, 28, 1, 16, 28, 3, 122, 11, 1, 7, 10, 49, 2, 4, 4, 3, 35, 2, 4, 15, 6, 36, 6]
	rankbased_samples = datas[0]
	rankbased_minRDs = datas[1]
	plt.subplot(144)
	plt.scatter(rankbased_samples, rankbased_minRDs, marker=".")

	# moconfig1_samples = [135.0, 136.0, 138.0, 140.0, 145.0, 147.0, 149.0, 151.0, 152.0]
	# moconfig1_minRDs = [48, 11, 54, 18, 5, 2, 23, 11, 12]
	moconfig1_samples = datas[2]
	moconfig1_minRDs = datas[3]
	plt.subplot(144)
	plt.scatter(moconfig1_samples, moconfig1_minRDs, marker="^")

	# moconfig2_samples = [329.0, 338.0, 340.0, 343.0, 345.0, 347.0, 349.0, 353.0, 355.0, 358.0, 361.0, 363.0, 364.0, 367.0, 371.0, 372.0, 373.0, 380.0, 382.0, 388.0, 389.0, 391.0, 393.0, 395.0, 398.0, 399.0, 402.0, 404.0, 407.0, 410.0, 412.0, 413.0, 417.0, 419.0, 420.0, 421.0, 423.0, 426.0, 428.0, 431.0, 433.0, 436.0, 439.0, 441.0, 445.0, 449.0, 450.0, 452.0, 455.0, 456.0, 458.0, 460.0, 461.0, 464.0, 467.0, 468.0, 470.0, 472.0, 479.0, 480.0, 485.0, 487.0, 489.0, 492.0, 497.0, 499.0, 502.0, 508.0, 509.0, 512.0, 517.0, 522.0, 524.0, 525.0, 529.0, 531.0, 535.0, 543.0, 545.0, 547.0, 550.0, 554.0, 557.0, 561.0, 563.0, 565.0, 567.0, 568.0, 572.0, 574.0, 576.0, 580.0, 581.0, 584.0, 586.0, 590.0, 594.0, 596.0, 597.0, 605.0]
	# moconfig2_minRDs = [11, 11, 7, 13, 42, 11, 8, 11, 11, 12, 12, 33, 11, 11, 11, 12, 9, 11, 11, 13, 12, 11, 15, 12, 13, 28, 7, 11, 13, 11, 12, 11, 11, 13, 62, 11, 12, 12, 13, 12, 12, 11, 12, 42, 11, 26, 11, 11, 13, 12, 11, 12, 13, 13, 29, 10, 11, 10, 12, 8, 11, 11, 1, 1, 11, 13, 11, 13, 49, 11, 13, 70, 8, 21, 13, 11, 12, 12, 25, 13, 11, 12, 8, 12, 12, 13, 9, 11, 8, 12, 11, 11, 11, 9, 11, 8, 13, 13, 12, 13]
	moconfig2_samples = datas[4]
	moconfig2_minRDs = datas[5]
	plt.subplot(144)
	plt.scatter(moconfig2_samples, moconfig2_minRDs, marker="+")

	# moconfig3_samples = [103.0, 94.0]
	# moconfig3_minRDs = [11, 14]
	moconfig3_samples = datas[6]
	moconfig3_minRDs = datas[7]
	plt.subplot(144)
	plt.scatter(moconfig3_samples, moconfig3_minRDs, marker="2")

	plt.xlabel("cost", fontsize=15)
	plt.ylabel("RD(10)", fontsize=15)
	plt.yscale("log") #### y = log(y)
	# plt.ylim([0.8, 50])
	# plt.xlim([0, 650])
	# plt.title("Predicted minRD of " + proj + " using the " + ga_method)
	plt.legend(["rank-based", "entropy-cost", "variance-cost", "density-cost"],
		# loc='upper center', bbox_to_anchor=(-0.6,0.95),ncol=3,fancybox=True,shadow=True
		)


	plt.tight_layout()
	plt.subplots_adjust(wspace=0.25)
	plt.savefig("pics/rq1/"+proj+".pdf")
	# plt.show()


def draw_combination_4(proj):
	import matplotlib.pyplot as plt

	plt.figure(figsize=(18,3.8))

	### 1. NSGA-II
	datas = compare_rank_based_with_moconfig(proj, "NSGAII")
	# rankbased_samples = [261, 220, 221, 222, 230, 216, 256, 237, 221, 269, 249, 229, 219, 249, 234, 237, 249, 216, 249, 257, 225, 255, 218, 220, 228, 306, 232, 235, 227, 234, 234, 223, 245, 216, 220, 227, 234, 233, 219, 232, 241, 246, 277, 238, 220, 237, 219, 238, 219, 260]	
	# rankbased_minRDs = [2, 41, 1, 46, 5, 50, 2, 93, 5, 4, 4, 45, 4, 2, 43, 9, 17, 2, 4, 1, 14, 23, 34, 5, 13, 2, 2, 1, 28, 1, 16, 28, 3, 122, 11, 1, 7, 10, 49, 2, 4, 4, 3, 35, 2, 4, 15, 6, 36, 6]
	rankbased_samples = datas[0]
	rankbased_minRDs = datas[1]
	plt.subplot(141)
	plt.scatter(rankbased_samples, rankbased_minRDs, marker=".")

	# moconfig1_samples = [135.0, 136.0, 138.0, 140.0, 145.0, 147.0, 149.0, 151.0, 152.0]
	# moconfig1_minRDs = [48, 11, 54, 18, 5, 2, 23, 11, 12]
	moconfig1_samples = datas[2]
	moconfig1_minRDs = datas[3]
	plt.subplot(141)
	plt.scatter(moconfig1_samples, moconfig1_minRDs, marker="^")

	# moconfig2_samples = [329.0, 338.0, 340.0, 343.0, 345.0, 347.0, 349.0, 353.0, 355.0, 358.0, 361.0, 363.0, 364.0, 367.0, 371.0, 372.0, 373.0, 380.0, 382.0, 388.0, 389.0, 391.0, 393.0, 395.0, 398.0, 399.0, 402.0, 404.0, 407.0, 410.0, 412.0, 413.0, 417.0, 419.0, 420.0, 421.0, 423.0, 426.0, 428.0, 431.0, 433.0, 436.0, 439.0, 441.0, 445.0, 449.0, 450.0, 452.0, 455.0, 456.0, 458.0, 460.0, 461.0, 464.0, 467.0, 468.0, 470.0, 472.0, 479.0, 480.0, 485.0, 487.0, 489.0, 492.0, 497.0, 499.0, 502.0, 508.0, 509.0, 512.0, 517.0, 522.0, 524.0, 525.0, 529.0, 531.0, 535.0, 543.0, 545.0, 547.0, 550.0, 554.0, 557.0, 561.0, 563.0, 565.0, 567.0, 568.0, 572.0, 574.0, 576.0, 580.0, 581.0, 584.0, 586.0, 590.0, 594.0, 596.0, 597.0, 605.0]
	# moconfig2_minRDs = [11, 11, 7, 13, 42, 11, 8, 11, 11, 12, 12, 33, 11, 11, 11, 12, 9, 11, 11, 13, 12, 11, 15, 12, 13, 28, 7, 11, 13, 11, 12, 11, 11, 13, 62, 11, 12, 12, 13, 12, 12, 11, 12, 42, 11, 26, 11, 11, 13, 12, 11, 12, 13, 13, 29, 10, 11, 10, 12, 8, 11, 11, 1, 1, 11, 13, 11, 13, 49, 11, 13, 70, 8, 21, 13, 11, 12, 12, 25, 13, 11, 12, 8, 12, 12, 13, 9, 11, 8, 12, 11, 11, 11, 9, 11, 8, 13, 13, 12, 13]
	moconfig2_samples = datas[4]
	moconfig2_minRDs = datas[5]
	plt.subplot(141)
	plt.scatter(moconfig2_samples, moconfig2_minRDs, marker="+")

	# moconfig3_samples = [103.0, 94.0]
	# moconfig3_minRDs = [11, 14]
	moconfig3_samples = datas[6]
	moconfig3_minRDs = datas[7]
	plt.subplot(141)
	plt.scatter(moconfig3_samples, moconfig3_minRDs, marker="2")

	plt.xlabel("cost", fontsize=15)
	plt.ylabel("RD(10)", fontsize=15)
	plt.yscale("log") #### y = log(y)
	# plt.ylim([0.8, 50])
	# plt.xlim([0, 500])
	plt.title("(a) MoConfig-NSGAII")
	plt.legend(["rank-based", "entropy-cost", "variance-cost", "density-cost"],
		# loc='upper center', bbox_to_anchor=(-0.6,0.95),ncol=3,fancybox=True,shadow=True
		)

	### 2. eMOEA
	datas = compare_rank_based_with_moconfig(proj, "eMOEA")
	# rankbased_samples = [261, 220, 221, 222, 230, 216, 256, 237, 221, 269, 249, 229, 219, 249, 234, 237, 249, 216, 249, 257, 225, 255, 218, 220, 228, 306, 232, 235, 227, 234, 234, 223, 245, 216, 220, 227, 234, 233, 219, 232, 241, 246, 277, 238, 220, 237, 219, 238, 219, 260]	
	# rankbased_minRDs = [2, 41, 1, 46, 5, 50, 2, 93, 5, 4, 4, 45, 4, 2, 43, 9, 17, 2, 4, 1, 14, 23, 34, 5, 13, 2, 2, 1, 28, 1, 16, 28, 3, 122, 11, 1, 7, 10, 49, 2, 4, 4, 3, 35, 2, 4, 15, 6, 36, 6]
	rankbased_samples = datas[0]
	rankbased_minRDs = datas[1]
	plt.subplot(142)
	plt.scatter(rankbased_samples, rankbased_minRDs, marker=".")

	# moconfig1_samples = [135.0, 136.0, 138.0, 140.0, 145.0, 147.0, 149.0, 151.0, 152.0]
	# moconfig1_minRDs = [48, 11, 54, 18, 5, 2, 23, 11, 12]
	moconfig1_samples = datas[2]
	moconfig1_minRDs = datas[3]
	plt.subplot(142)
	plt.scatter(moconfig1_samples, moconfig1_minRDs, marker="^")

	# moconfig2_samples = [329.0, 338.0, 340.0, 343.0, 345.0, 347.0, 349.0, 353.0, 355.0, 358.0, 361.0, 363.0, 364.0, 367.0, 371.0, 372.0, 373.0, 380.0, 382.0, 388.0, 389.0, 391.0, 393.0, 395.0, 398.0, 399.0, 402.0, 404.0, 407.0, 410.0, 412.0, 413.0, 417.0, 419.0, 420.0, 421.0, 423.0, 426.0, 428.0, 431.0, 433.0, 436.0, 439.0, 441.0, 445.0, 449.0, 450.0, 452.0, 455.0, 456.0, 458.0, 460.0, 461.0, 464.0, 467.0, 468.0, 470.0, 472.0, 479.0, 480.0, 485.0, 487.0, 489.0, 492.0, 497.0, 499.0, 502.0, 508.0, 509.0, 512.0, 517.0, 522.0, 524.0, 525.0, 529.0, 531.0, 535.0, 543.0, 545.0, 547.0, 550.0, 554.0, 557.0, 561.0, 563.0, 565.0, 567.0, 568.0, 572.0, 574.0, 576.0, 580.0, 581.0, 584.0, 586.0, 590.0, 594.0, 596.0, 597.0, 605.0]
	# moconfig2_minRDs = [11, 11, 7, 13, 42, 11, 8, 11, 11, 12, 12, 33, 11, 11, 11, 12, 9, 11, 11, 13, 12, 11, 15, 12, 13, 28, 7, 11, 13, 11, 12, 11, 11, 13, 62, 11, 12, 12, 13, 12, 12, 11, 12, 42, 11, 26, 11, 11, 13, 12, 11, 12, 13, 13, 29, 10, 11, 10, 12, 8, 11, 11, 1, 1, 11, 13, 11, 13, 49, 11, 13, 70, 8, 21, 13, 11, 12, 12, 25, 13, 11, 12, 8, 12, 12, 13, 9, 11, 8, 12, 11, 11, 11, 9, 11, 8, 13, 13, 12, 13]
	moconfig2_samples = datas[4]
	moconfig2_minRDs = datas[5]
	plt.subplot(142)
	plt.scatter(moconfig2_samples, moconfig2_minRDs, marker="+")

	# moconfig3_samples = [103.0, 94.0]
	# moconfig3_minRDs = [11, 14]
	moconfig3_samples = datas[6]
	moconfig3_minRDs = datas[7]
	plt.subplot(142)
	plt.scatter(moconfig3_samples, moconfig3_minRDs, marker="2")

	plt.xlabel("cost", fontsize=15)
	plt.ylabel("RD(10)", fontsize=15)
	plt.yscale("log") #### y = log(y)
	# plt.ylim([0.8, 50])
	# plt.xlim([0, 500])
	plt.title("(b) MoConfig-eMOEA")
	plt.legend(["rank-based", "entropy-cost", "variance-cost", "density-cost"],
		# loc='upper center', bbox_to_anchor=(-0.6,0.95),ncol=3,fancybox=True,shadow=True
		)

	### 3. IBEA
	datas = compare_rank_based_with_moconfig(proj, "IBEA")
	# rankbased_samples = [261, 220, 221, 222, 230, 216, 256, 237, 221, 269, 249, 229, 219, 249, 234, 237, 249, 216, 249, 257, 225, 255, 218, 220, 228, 306, 232, 235, 227, 234, 234, 223, 245, 216, 220, 227, 234, 233, 219, 232, 241, 246, 277, 238, 220, 237, 219, 238, 219, 260]	
	# rankbased_minRDs = [2, 41, 1, 46, 5, 50, 2, 93, 5, 4, 4, 45, 4, 2, 43, 9, 17, 2, 4, 1, 14, 23, 34, 5, 13, 2, 2, 1, 28, 1, 16, 28, 3, 122, 11, 1, 7, 10, 49, 2, 4, 4, 3, 35, 2, 4, 15, 6, 36, 6]
	rankbased_samples = datas[0]
	rankbased_minRDs = datas[1]
	plt.subplot(143)
	plt.scatter(rankbased_samples, rankbased_minRDs, marker=".")

	# moconfig1_samples = [135.0, 136.0, 138.0, 140.0, 145.0, 147.0, 149.0, 151.0, 152.0]
	# moconfig1_minRDs = [48, 11, 54, 18, 5, 2, 23, 11, 12]
	moconfig1_samples = datas[2]
	moconfig1_minRDs = datas[3]
	plt.subplot(143)
	plt.scatter(moconfig1_samples, moconfig1_minRDs, marker="^")

	# moconfig2_samples = [329.0, 338.0, 340.0, 343.0, 345.0, 347.0, 349.0, 353.0, 355.0, 358.0, 361.0, 363.0, 364.0, 367.0, 371.0, 372.0, 373.0, 380.0, 382.0, 388.0, 389.0, 391.0, 393.0, 395.0, 398.0, 399.0, 402.0, 404.0, 407.0, 410.0, 412.0, 413.0, 417.0, 419.0, 420.0, 421.0, 423.0, 426.0, 428.0, 431.0, 433.0, 436.0, 439.0, 441.0, 445.0, 449.0, 450.0, 452.0, 455.0, 456.0, 458.0, 460.0, 461.0, 464.0, 467.0, 468.0, 470.0, 472.0, 479.0, 480.0, 485.0, 487.0, 489.0, 492.0, 497.0, 499.0, 502.0, 508.0, 509.0, 512.0, 517.0, 522.0, 524.0, 525.0, 529.0, 531.0, 535.0, 543.0, 545.0, 547.0, 550.0, 554.0, 557.0, 561.0, 563.0, 565.0, 567.0, 568.0, 572.0, 574.0, 576.0, 580.0, 581.0, 584.0, 586.0, 590.0, 594.0, 596.0, 597.0, 605.0]
	# moconfig2_minRDs = [11, 11, 7, 13, 42, 11, 8, 11, 11, 12, 12, 33, 11, 11, 11, 12, 9, 11, 11, 13, 12, 11, 15, 12, 13, 28, 7, 11, 13, 11, 12, 11, 11, 13, 62, 11, 12, 12, 13, 12, 12, 11, 12, 42, 11, 26, 11, 11, 13, 12, 11, 12, 13, 13, 29, 10, 11, 10, 12, 8, 11, 11, 1, 1, 11, 13, 11, 13, 49, 11, 13, 70, 8, 21, 13, 11, 12, 12, 25, 13, 11, 12, 8, 12, 12, 13, 9, 11, 8, 12, 11, 11, 11, 9, 11, 8, 13, 13, 12, 13]
	moconfig2_samples = datas[4]
	moconfig2_minRDs = datas[5]
	plt.subplot(143)
	plt.scatter(moconfig2_samples, moconfig2_minRDs, marker="+")

	# moconfig3_samples = [103.0, 94.0]
	# moconfig3_minRDs = [11, 14]
	moconfig3_samples = datas[6]
	moconfig3_minRDs = datas[7]
	plt.subplot(143)
	plt.scatter(moconfig3_samples, moconfig3_minRDs, marker="2")

	plt.xlabel("cost", fontsize=15)
	plt.ylabel("RD(10)", fontsize=15)
	plt.yscale("log") #### y = log(y)
	# plt.ylim([0.8, 50])
	# plt.xlim([0, 500])
	plt.title("(c) MoConfig-IBEA")
	plt.legend(["rank-based", "entropy-cost", "variance-cost", "density-cost"],
		# loc='upper center', bbox_to_anchor=(-0.6,0.95),ncol=3,fancybox=True,shadow=True
		)

	### 4. DBEA
	datas = compare_rank_based_with_moconfig(proj, "DBEA")
	# rankbased_samples = [261, 220, 221, 222, 230, 216, 256, 237, 221, 269, 249, 229, 219, 249, 234, 237, 249, 216, 249, 257, 225, 255, 218, 220, 228, 306, 232, 235, 227, 234, 234, 223, 245, 216, 220, 227, 234, 233, 219, 232, 241, 246, 277, 238, 220, 237, 219, 238, 219, 260]	
	# rankbased_minRDs = [2, 41, 1, 46, 5, 50, 2, 93, 5, 4, 4, 45, 4, 2, 43, 9, 17, 2, 4, 1, 14, 23, 34, 5, 13, 2, 2, 1, 28, 1, 16, 28, 3, 122, 11, 1, 7, 10, 49, 2, 4, 4, 3, 35, 2, 4, 15, 6, 36, 6]
	rankbased_samples = datas[0]
	rankbased_minRDs = datas[1]
	plt.subplot(144)
	plt.scatter(rankbased_samples, rankbased_minRDs, marker=".")

	# moconfig1_samples = [135.0, 136.0, 138.0, 140.0, 145.0, 147.0, 149.0, 151.0, 152.0]
	# moconfig1_minRDs = [48, 11, 54, 18, 5, 2, 23, 11, 12]
	moconfig1_samples = datas[2]
	moconfig1_minRDs = datas[3]
	plt.subplot(144)
	plt.scatter(moconfig1_samples, moconfig1_minRDs, marker="^")

	# moconfig2_samples = [329.0, 338.0, 340.0, 343.0, 345.0, 347.0, 349.0, 353.0, 355.0, 358.0, 361.0, 363.0, 364.0, 367.0, 371.0, 372.0, 373.0, 380.0, 382.0, 388.0, 389.0, 391.0, 393.0, 395.0, 398.0, 399.0, 402.0, 404.0, 407.0, 410.0, 412.0, 413.0, 417.0, 419.0, 420.0, 421.0, 423.0, 426.0, 428.0, 431.0, 433.0, 436.0, 439.0, 441.0, 445.0, 449.0, 450.0, 452.0, 455.0, 456.0, 458.0, 460.0, 461.0, 464.0, 467.0, 468.0, 470.0, 472.0, 479.0, 480.0, 485.0, 487.0, 489.0, 492.0, 497.0, 499.0, 502.0, 508.0, 509.0, 512.0, 517.0, 522.0, 524.0, 525.0, 529.0, 531.0, 535.0, 543.0, 545.0, 547.0, 550.0, 554.0, 557.0, 561.0, 563.0, 565.0, 567.0, 568.0, 572.0, 574.0, 576.0, 580.0, 581.0, 584.0, 586.0, 590.0, 594.0, 596.0, 597.0, 605.0]
	# moconfig2_minRDs = [11, 11, 7, 13, 42, 11, 8, 11, 11, 12, 12, 33, 11, 11, 11, 12, 9, 11, 11, 13, 12, 11, 15, 12, 13, 28, 7, 11, 13, 11, 12, 11, 11, 13, 62, 11, 12, 12, 13, 12, 12, 11, 12, 42, 11, 26, 11, 11, 13, 12, 11, 12, 13, 13, 29, 10, 11, 10, 12, 8, 11, 11, 1, 1, 11, 13, 11, 13, 49, 11, 13, 70, 8, 21, 13, 11, 12, 12, 25, 13, 11, 12, 8, 12, 12, 13, 9, 11, 8, 12, 11, 11, 11, 9, 11, 8, 13, 13, 12, 13]
	moconfig2_samples = datas[4]
	moconfig2_minRDs = datas[5]
	plt.subplot(144)
	plt.scatter(moconfig2_samples, moconfig2_minRDs, marker="+")

	# moconfig3_samples = [103.0, 94.0]
	# moconfig3_minRDs = [11, 14]
	moconfig3_samples = datas[6]
	moconfig3_minRDs = datas[7]
	plt.subplot(144)
	plt.scatter(moconfig3_samples, moconfig3_minRDs, marker="2")

	plt.xlabel("cost", fontsize=15)
	plt.ylabel("RD(10)", fontsize=15)
	plt.yscale("log") #### y = log(y)
	# plt.ylim([0.8, 50])
	# plt.xlim([0, 500])
	plt.title("(d) MoConfig-DBEA")
	plt.legend(["rank-based", "entropy-cost", "variance-cost", "density-cost"],
		# loc='upper center', bbox_to_anchor=(-0.6,0.95),ncol=3,fancybox=True,shadow=True
		)

	plt.tight_layout()
	plt.subplots_adjust(wspace=0.25)
	plt.savefig("pics/rq2/"+proj+".jpg")
	# plt.show()



if __name__ == "__main__":
	##  >>> basic information of each dataset
	# search_raw_data("raw_data/")

	## >>> split the dataset into training, validation and test pool by 2:1:2

	# subtrain + validation set using rank based
	# cost_data = get_whole_combined_sub_train_size()
	# draw_combine_train(cost_data)

	## minRD using rank based
	# rd_data = get_whole_minRD(10)
	# draw_rank_based_minRD(rd_data)

	## mmre using rank based
	# mmre_data = get_whole_mmre()
	# draw_rank_based_mmre(mmre_data)

	# read the eclipse results and show the objective values of each dataset  
	projs, datas = read_eclipse_results("eclipse_results.txt") # path should be changed in different environments
	print(projs)
	# print(projs[0], datas[0])
	# proj_names = ['rs-6d-c3-obj1_0.csv', 'rs-6d-c3-obj2_0.csv', 'snw_0.csv', 'sol-6d-c2-obj1_0.csv', 'sol-6d-c2-obj2_0.csv', 'wc+rs-3d-c4-obj1_0.csv', 'wc+rs-3d-c4-obj2_0.csv', 'wc+sol-3d-c4-obj1_0.csv', 'wc+sol-3d-c4-obj2_0.csv', 'wc+wc-3d-c4-obj1_0.csv', 'wc+wc-3d-c4-obj2_0.csv', 'wc-3d-c4-obj1_0.csv', 'wc-3d-c4-obj2_0.csv', 'wc-5d-c5-obj1_0.csv', 'wc-5d-c5-obj2_0.csv', 'wc-6d-c1-obj1_0.csv', 'wc-6d-c1-obj2_0.csv', 'wc-c1-3d-c1-obj1_0.csv', 'wc-c1-3d-c1-obj2_0.csv', 'wc-c3-3d-c1-obj1_0.csv', 'wc-c3-3d-c1-obj2_0.csv']
	# draw_multi_obj(projs[0], datas[0])
	# for i in range(len(projs)):
	# 	draw_multi_obj(projs[i], datas[i])

	# read the moConfig results and draw the RD and COST figures of each dataset
	# files = [f for f in os.listdir("raw_data/") if f.endswith(".csv")]
	# ga_method = "NSGAII"
	# # ga_method = "eMOEA"
	# # ga_method = "IBEA"
	# # ga_method = "DBEA"
	# for file in files[:1]:
		# proj = file[:-4]
		# draw_comparision_minRD(proj, ga_method)
		# table_comparision_minRD(proj, ga_method)

	ga_method = "NSGAII"
	for i in range(len(projs))[5:6]:
		# draw_combination_3_1(projs[i][:-6], datas[i], ga_method)
		draw_combination_4(projs[i][:-6])


	## record the time cost of MoConfig
	# get_time_cost()

