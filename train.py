#! /usr/bin/env python
# coding: utf-8


from cabocha.analyzer import CaboChaAnalyzer


class Tokenizer:
    def __init__(self):
        self._analyzer = CaboChaAnalyzer()

    def tokenize(self, text):
        return self._analyzer.analyze(text).wakati.split(" ")


if __name__ == "__main__":
    import pandas as pd

    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GridSearchCV
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import Pipeline

    frame = pd.read_table("test.csv", sep=",")

    X = frame["sent"]
    y = frame["name"]

    X_train, X_test, y_train, y_test = train_test_split(X, y)
    print(X_train.head())
    print(y_train.head())

    tokenizer = Tokenizer()

    pipe = Pipeline([("vectorizer", CountVectorizer(tokenizer=tokenizer.tokenize)),
                     ("logistic", LogisticRegression)])
    params = {"logistic__C": [0.01, 0.1, 1, 10, 100]}
    grid = GridSearchCV(pipe, param_grid=params)
    print("training ...")
    grid.fit(X_train, y_train)
    print("training ... done")
    print("Train score: {}".format(grid.score(X_train, y_train)))
    print("Test score: {}".format(grid.score(X_test, _y_test)))