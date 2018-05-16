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
    import pickle

    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GridSearchCV
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import Pipeline

    # load dataet
    dataset = pickle.load(open("dataset.pkl", "rb"))

    # split train/test dataset
    X, y = dataset.data, dataset.target
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    print("Dataset size: {}, train: {}, test: {}".format(X.shape[0], X_train.shape[0], X_test.shape[0]))

    # prepare tokenizer
    tokenizer = Tokenizer()

    # create pipeline
    pipe = Pipeline([("vectorizer", CountVectorizer()), 
                     ("logistic", LogisticRegression())])
    params = {"vectorizer__tokenizer": [tokenizer.tokenize],
              "logistic__C": [0.01, 0.1, 1, 10, 100]}
    grid = GridSearchCV(pipe, param_grid=params)
    print("training ...")
    grid.fit(X_train, y_train)
    print("training ... done")
    print("Best parameter: {}".format(grid.best_params_))
    print(pd.DataFrame(grid.cv_results_))
    print("Train score: {}".format(grid.score(X_train, y_train)))

    # final model
    print("Training best model")
    grid.fit(X_train, y_train)
    grid.score(X_test, y_test)
    print("Test score: {}".format(grid.score(X_test, y_test)))