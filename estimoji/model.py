#! /usr/bin/env python
# coding: utf-8

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from estimoji.util import load_emoji_id
from estimoji.util import Tokenizer
import pickle


def load_model(modelname):
    pipe = pickle.load(open(modelname, "br"))
    return pipe