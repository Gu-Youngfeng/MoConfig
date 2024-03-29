# MoConfig

This project shows the prototype **MoConfig**.
[MoConfigSampling](MoConfigSampling/) (in Java) and [MoConfigComparison](MoConfigComparison/) (in Python) are two main parts, implementing the process of MoConfig sampling and the comparasion with the rank-based method, respectively.

### 1. Dataset and environments

The 20 raw datasets we used are saved in the directory **MoConfigComparison/raw_data/**. 

The environments of MoConfig project includes JDK 1.7/1.8, Python 3.X. Moreover, `sklearn`, `pandas`, `numpy` libraries should also be installed.


### 2. Experiment steps

_Step 1:_ We run the rank-based method to divide each dataset into the training pool, validation pool, and test pool.
Above sets are generated and saved in the directory **MoConfigComparison/parse_data/**.

_Step 2:_ We combine the training pool and validation pool generated by rank-based method into a combiantion dataset (**MoConfigComparison/parse_data/combined_train/**).
We copy this combination dataset to the directory **MoConfigSampling/testbed/input/** and take it as the input of MoConfig.

_Step 3:_ We run the MoConfig to sample the optimal sampling sets from the training pool. 
The optimal sampling sets are saved in the directory **MoConfigSampling/testbed/output/**.

_Step 4:_ We find the best configuration based on the sampling sets generated by MoConfig. 
The prediction results are saved in **MoConfigComparison/experiments/moconfig/**.

_Step 5:_ We compare the results between the rank-based and MoConfig methods.
The visualized results of comparision are saved in **MoConfigComparison/pics/**.


### 3. Implementation

Here, we list the related code entries to above steps. For instance, we just run the main function in `rankbased.py` to implement the Step 1 and Step 2.

|Step|Running entry|Time cost|
|:--|:--|:--|
|1,2|`MoConfigComparison/rankbased.py`|Around 150 seconds|
|3  |`MoConfigSampling/src/main/java/cn/edu/whu/cstar/experiments/Launcher.java`|Around 20 minutes|
|4  |`MoConfigComparison/moconfig.py`|Around 40 minutes|
|5  |`MoConfigComparison/experiments.py`|Arounds 150 seconds|

