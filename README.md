# chefboost

<p align="center"><img src="https://raw.githubusercontent.com/serengil/chefboost/master/icon/chefboost.jpg" width="200" height="200"></p>

Chefboost is [gradient boosting](https://sefiks.com/2018/10/04/a-step-by-step-gradient-boosting-decision-tree-example/), [random forest](https://sefiks.com/2017/11/19/how-random-forests-can-keep-you-from-decision-tree/) and [adaboost](https://sefiks.com/2018/11/02/a-step-by-step-adaboost-example/) enabled decision tree framework including regular [ID3](https://sefiks.com/2017/11/20/a-step-by-step-id3-decision-tree-example/), [C4.5](https://sefiks.com/2018/05/13/a-step-by-step-c4-5-decision-tree-example/), [CART](https://sefiks.com/2018/08/27/a-step-by-step-cart-decision-tree-example/) and [regression tree](https://sefiks.com/2018/08/28/a-step-by-step-regression-decision-tree-example/) algorithms **with categorical features support**.

# Usage

Basically, you just need to pass the dataset as pandas data frame and tree configurations after importing Chefboost as illustrated below. You just need to set the label of the target column to **Decision**. Besides, chefboost handles both numeric and nominal features and target values in contrast to its alternatives.

```
import Chefboost as chef
import pandas as pd

config = {
	'algorithm': 'ID3' #ID3, C4.5, CART, Regression
	, 'enableGBM': False, 'epochs': 10, 'learning_rate': 1
	, 'enableRandomForest': False, 'num_of_trees': 5, 'enableMultitasking': False
	, 'enableAdaboost': False
	, 'debug': False
}

df = pd.read_csv("dataset/golf3.txt")

chef.fit(df, config)
```

Initial tests are run on Python 3.6.4 and Windows 10 OS.

# Outcomes

Built decision trees are stored as python if statements in the `outputs/rules/rules.py` file. A sample of decision rules is demonstrated below.

```
def findDecision(Outlook,Temperature,Humidity,Wind,Decision):
   if Outlook == 'Rain':
      if Wind == 'Weak':
         return 'Yes'
      if Wind == 'Strong':
         return 'No'
   if Outlook == 'Sunny':
      if Humidity == 'High':
         return 'No'
      if Humidity == 'Normal':
         return 'Yes'
   if Outlook == 'Overcast':
      return 'Yes'
 ```

# Prerequisites

Pandas and numpy python libraries are used to load data sets in this repository. You might run the following commands to install these packages if you are going to use them first time.

```
pip install pandas
pip install numpy
```

# Documentation

You can find detailed documentations about these core algorithms [here](https://sefiks.com/tag/decision-tree/).

# Licence

Chefboost is licensed under the MIT License - see [`LICENSE`](https://github.com/serengil/chefboost/blob/master/LICENSE) for more details.
