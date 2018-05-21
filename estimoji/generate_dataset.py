#! /usr/bin/env python
# coding: utf-8

import sys
import os
import pickle
import pandas as pd
from sklearn.utils import Bunch
from estimoji.util import load_emoji_id
from estimoji.util import extract_emoji


def generate(out, csv=None, stats=None):
    """学習データを生成する
    Args:
        out (str): pickle 形式の学習データを保存するファイル名。必ず指定する
        csv (str): CSV形式の学習データを保存するファイル名。指定しなければ保存されない
        stats (str): 絵文字の頻度情報を保存するファイル名。指定しなければ保存されない
    """
    # 学習に使う絵文字リストをロード
    emoji_id = load_emoji_id()

    # 学習データのロード
    items = []
    num_data = 0
    num_train = 0
    for line in sys.stdin:
        text = line.strip("\n")
        split_items = extract_emoji(text)
        for sent, emoji_set in split_items.items():
            for emoji_ in emoji_set:
                num_data += 1
                # 学習に利用する絵文字であれば学習データに追加
                if emoji_ in emoji_id:
                    num_train += 1
                    items.append((emoji_, emoji_id[emoji_], sent))
    frame = pd.DataFrame(items, columns=["emoji", "label", "sent"])
    assert frame.shape[0] == num_train
    print("Data size: {}, after filtering: {}".format(num_data, num_train))

    # 学習データの絵文字の頻度データをファイルにダンプ
    if stats:
        emojis = frame["emoji"].value_counts()
        print("Saving emoji frequency data in {} ...".format(stats))
        emojis.to_csv(stats, sep="\t")
        print("Saving emoji frequency data in {} ... done".format(stats))

    # 正解ラベルを生成
    if csv:
        print("Saving data in {} ...".format(csv))
        frame.to_csv(csv)
        print("Saving data in {} ... done".format(csv))

    # データセットを作成
    target_names = [emoji for emoji, id_ in
                    sorted(emoji_id.items(), key=lambda item: item[1])]
    dataset = Bunch(data=frame["sent"].values,
                    target=frame["emoji"].values,
                    feature_names=["sent"],
                    target_names=target_names)

    print("Saving dataset in {} ...".format(out))
    pickle.dump(dataset, open(out, "wb"))
    print("Saving dataset in {} ... done".format(out))


if __name__ == "__main__":
    import fire

    fire.Fire(generate)