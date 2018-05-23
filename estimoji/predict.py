#! /usr/bin/env python
# coding: utf-8

import sys
from estimoji.model import load_model


def estimate(model):
    """
    Args:
        model (str): モデルファイルのファイル名
    """
    # emoji_id = load_emoji_id()
    pipe = load_model(model)
    for line in sys.stdin:
        text = line.strip("\n")
        probs = pipe.predict_proba([text])[0]
        sorted_res = sorted(zip(probs, pipe.classes_),
                            key=lambda item: item[0],
                            reverse=True)
        for prob, emoji in list(sorted_res)[:5]:
            print("{:.4f} {}".format(prob, emoji))


if __name__ == "__main__":
    import fire

    fire.Fire(estimate)