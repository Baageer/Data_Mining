import os
import pandas as pd
import numpy as np
from collections import defaultdict
from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import cross_val_score

data_filename ="datas/201311.csv"
data_folder = "datas"

dataset = pd.read_csv(data_filename, parse_dates=[0],
                      skiprows=[0,])
dataset.columns = ["Date", "Start (ET)", "Visitor Team", "VisitorPts",
                   "Home Team", "HomePts","Score Type", "OT?", "Notes"]


dataset["HomeWin"] = dataset["VisitorPts"] < dataset["HomePts"]
dataset["HomeLastWin"] = ""
dataset["VisitorLastWin"] = ""
y_true = dataset["HomeWin"].values

won_last = defaultdict(int)
for index, row in dataset.iterrows():
    #print('row', row)
    home_team = row["Home Team"]
    visitor_team = row["Visitor Team"]
    row["HomeLastWin"] = won_last[home_team]
    row["VisitorLastWin"] = won_last[visitor_team]
    print(home_team, won_last[home_team])
    dataset.ix[index] = row
    won_last[home_team] = row["HomeWin"]
    won_last[visitor_team] = not row["HomeWin"]
    #print(row)

#print (dataset.ix[10:15])

clf = DecisionTreeClassifier(random_state=14)
X_previouswins = dataset[["HomeLastWin","VisitorLastWin"]].values

scores = cross_val_score(clf, X_previouswins, y_true, scoring='accuracy')
print("Accuracy: {0:.1f}%".format(np.mean(scores)*100 ))


standings_filename = os.path.join(data_folder,
                                  "NBA_2013_Expanded_Standings.csv")
standings = pd.read_csv(standings_filename, skiprows=[0,1])
standings.columns = ["Rk", "Team", "Overall", "Home", "Road", "E", "W", "A",
                     "C", "SE", "NW", "P", "SW", "Pre", "Post", "≤3", "≥10",
                     "Otc", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr"]
#print(standings)

dataset["HomeTeamRanksHigher"] = 0
for index, row in dataset.iterrows():
    home_team = row["Home Team"]
    visitor_team = row["Visitor Team"]
    if home_team == "New Orleans Pelicans":
        home_team = "New Orleans Hornets"
    elif visitor_team == "New Orleans Pelicans":
        visitor_team = "New Orleans Hornets"
    home_rank = standings[standings["Team"]==home_team]["Rk"].values[0]
    visitor_rank = standings[standings["Team"]==visitor_team]["Rk"].values[0]
    row["HomeTeamRanksHigher"] = int(home_rank>visitor_rank)
    dataset.ix[index] = row

X_homehigher = dataset[ ["HomeLastWin", "VisitorLastWin",
                         "HomeTeamRanksHigher"] ].values

clf_1 = DecisionTreeClassifier(random_state=14)
scores_1 = cross_val_score(clf_1, X_homehigher, y_true, scoring='accuracy_1')
print("Accuracy_1: {0:.1f}%".format(np.mean(scores_1)*100 ))
