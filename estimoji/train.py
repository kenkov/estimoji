#! /usr/bin/env python
# coding: utf-8

import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from estimoji.util import Tokenizer


def train(dataset, out, random_state=0):
    """学習する

    Args:
        dataset (str): pickle フォーマットの学習データファイル名
        out (str): 保存する学習モデルのファイル名
        ramdom_state (int): ランダムシード
    """
    # load dataet
    dataset = pickle.load(open("dataset.pkl", "rb"))

    # split train/test dataset
    X, y = dataset.data[:100], dataset.target[:100]
    print(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=random_state)
    print("Dataset size: {}, train: {}, test: {}".format(X.shape[0],
                                                         X_train.shape[0],
                                                         X_test.shape[0]))

    # prepare tokenizer
    tokenizer = Tokenizer()

    # create pipeline
    pipe = Pipeline([("vectorizer", CountVectorizer()), 
                     ("logistic", LogisticRegression())])
    params = {"vectorizer__tokenizer": [tokenizer.tokenize],
              "vectorizer__ngram_range": [(1, 1)],
              "logistic__C": [0.01, 0.1, 1, 10, 100],
              "logistic__random_state": [random_state]}
    grid = GridSearchCV(pipe, param_grid=params)
    print("training ...")
    grid.fit(X_train, y_train)
    print("training ... done")
    print("Best parameter: {}".format(grid.best_params_))
    print("Best cross-validation score: {}".format(grid.best_score_))

    # final model
    print("Training best model")
    best_params = grid.best_params_
    pipe = Pipeline([("vectorizer", CountVectorizer(tokenizer=best_params["vectorizer__tokenizer"],
                                                    ngram_range=best_params["vectorizer__ngram_range"])), 
                     ("logistic", LogisticRegression(C=best_params["logistic__C"],
                                                     random_state=best_params["logistic__random_state"]))])
    pipe.fit(X_train, y_train)
    pipe.score(X_test, y_test)
    print("Test score: {}".format(grid.score(X_test, y_test)))

    print("Saving model ...")
    pickle.dump(pipe, open(out, "wb"))
    print("Saving model ... done")



if __name__ == "__main__":
    import fire

    fire.Fire(train)