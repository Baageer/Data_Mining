import pandas as pd
import numpy as np
from collections import defaultdict
from sklearn.tree import DecisionTreeClassifier

data_filename ="datas/201310.csv"

dataset = pd.read_csv(data_filename, parse_dates=[0],
                      skiprows=[0,])
dataset.columns = ["Date", "Start (ET)", "Visitor Team", "VisitorPts",
                   "Home Team", "HomePts","Score Type", "OT?", "Notes"]

dataset["HomeWin"] = dataset["VisitorPts"] < dataset["HomePts"]
y_true = dataset["HomeWin"].values

won_last = defaultdict(int)
for index, row in dataset.iterrows():
    home_team = row["Home Team"]
    visitor_team = row["Visitor Team"]
    row["HomeLastWin"] = won_last[home_team]
    row["VisitorLastWin"] = won_last[visitor_team]
    dataset.ix[index] = row
    won_last[home_team] = row["HomeWin"]
    won_last[visitor_team] = not row["HomeWin"]
    print(won_last)

#print (dataset.ix[10:15])

clf = DecisionTreeClassifier(random_state=14)
X_previouswins = dataset[["HomeLastWin","VisitorLastWin"]].values

scores = cross_val_score(cls, X_previouswins, y_ture, scoring='accuracy')
print("Accuracy: {0:.1f}%".format(np.mean(scores)*100 ))
