import os
import pandas as pd
import numpy as np
from collections import defaultdict
from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.grid_search import GridSearchCV


data_filename ="datas/201311.csv"
data_folder = "datas"

dataset = pd.read_csv(data_filename, parse_dates=[0])
dataset.columns = ["Date", "Start (ET)", "Visitor Team", "VisitorPts",
                   "Home Team", "HomePts","Score Type", "OT?", "Notes"]


dataset["HomeWin"] = dataset["VisitorPts"] < dataset["HomePts"]
dataset["HomeLastWin"] = ""
dataset["VisitorLastWin"] = ""
y_true = dataset["HomeWin"].values
#print(dataset)

won_last = defaultdict(int)
for index, row in dataset.iterrows():
    #print('row', row)
    home_team = row["Home Team"]
    visitor_team = row["Visitor Team"]
    row["HomeLastWin"] = won_last[home_team]
    row["VisitorLastWin"] = won_last[visitor_team]
    #print(home_team, won_last[home_team])
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
standings = pd.read_csv(standings_filename)
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
    #print('a', home_team, visitor_team)
    #print('b\n', standings["Team"]==visitor_team)
    home_rank = standings[standings["Team"]==home_team]["Rk"].values[0]
    visitor_rank = standings[standings["Team"]==visitor_team]["Rk"].values[0]
    row["HomeTeamRanksHigher"] = int(home_rank>visitor_rank)
    dataset.ix[index] = row

X_homehigher = dataset[ ["HomeLastWin", "VisitorLastWin",
                         "HomeTeamRanksHigher"] ].values

clf_1 = DecisionTreeClassifier(random_state=14)
scores_1 = cross_val_score(clf_1, X_homehigher, y_true, scoring='accuracy')
print("Accuracy_1: {0:.1f}%".format(np.mean(scores_1)*100 ))


last_match_winner = defaultdict(int)
dataset["HomeTeamWonLast"] = 0
for index, row in dataset.iterrows():
    home_team = row["Home Team"]
    visitor_team = row["Visitor Team"]
    teams = tuple(sorted([home_team, visitor_team]))
    row["HomeTeamWonLast"] = 1 if last_match_winner[teams] == row["Home Team"] else 0
    dataset.ix[index] = row
    winner = row["Home Team"] if row["HomeWin"] else row["Visitor Team"]
    last_match_winner[teams] = winner

X_lastwinner = dataset[["HomeTeamRanksHigher", "HomeTeamWonLast"]].values
clf2 = DecisionTreeClassifier(random_state=14)
scores2 = cross_val_score(clf2, X_lastwinner, y_true, scoring='accuracy')
print("Accuracy_2: {0:.1f}%".format(np.mean(scores2)*100 ))

encoding = LabelEncoder()
encoding.fit(dataset["Home Team"].values)
home_teams = encoding.transform(dataset["Home Team"].values)
visitor_teams = encoding.transform(dataset["Visitor Team"].values)
X_teams = np.vstack([home_teams, visitor_teams]).T

onehot = OneHotEncoder()
X_teams_expanded = onehot.fit_transform(X_teams).todense()
clf3 = DecisionTreeClassifier(random_state=14)
scores3 = cross_val_score(clf3, X_teams_expanded, y_true, scoring='accuracy')
print("Accuracy_3: {0:.1f}%".format(np.mean(scores3)*100))


clf4 = RandomForestClassifier(random_state=14)
scores4 = cross_val_score(clf4, X_teams, y_true, scoring='accuracy')
print("Accuracy_4: {0:.1f}%".format(np.mean(scores4)*100 ))

X_all = np.hstack([X_lastwinner, X_teams])
clf5 = RandomForestClassifier(random_state=14)
scores5 = cross_val_score(clf5, X_all, y_true, scoring='accuracy')
print("Accuracy_5: {0:.1f}%".format(np.mean(scores5)*100 ))

parameter_space = {
    "max_features": [2, 10, 'auto'],
    "n_estimators": [100,],
    "criterion": ["gini", "entropy"],
    "min_samples_leaf": [2, 4, 6],
    }
clf6 = RandomForestClassifier(random_state=14)
grid = GridSearchCV(clf6, parameter_space)
grid.fit(X_all, y_true)
print("Accuracy_6: {0:.1f}%".format(grid.best_score_ * 100))
