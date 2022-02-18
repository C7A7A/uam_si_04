import pickle
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn import tree as tr

def train():
    col_names = ['water', 'fertilizer', 'seeds', 'capacity', 'distance_from_center', 'action']
    panda = pd.read_csv("tree_data.csv", header=0, names=col_names, sep=';')
    X = panda[col_names[:-1]]
    y = panda.action

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state=0)

    tree = DecisionTreeClassifier()

    tree = tree.fit(X_train, y_train)

    y_pred = tree.predict(X_test)
    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
    text_representation = tr.export_text(tree, feature_names=col_names[:-1])
    print(text_representation)
    return tree

with open('tree_classifier.pkl', 'wb') as file:
    pickle.dump(train(), file)
