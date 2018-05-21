#! /usr/bin/env python
# coding: utf-8

import pickle
import sys
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from estimoji.util import load_emoji_id
from estimoji.util import Tokenizer


def load_model(modelname):
    pipe = pickle.load(open(modelname, "br"))
    return pipe


def estimate(model):
    """
    Args:
        model (str): モデルファイルのファイル名
    """
    # emoji_id = load_emoji_id()
    pipe = load_model(model)
    for line in sys.stdin:
        text = line.strip("\n")
        res = pipe.predict_proba([text])
        print(res)
        # name = dataset.target_names[res[0]]
        # print(emoji.EMOJI_UNICODE[name])


if __name__ == "__main__":
    import fire

    fire.Fire(estimate)