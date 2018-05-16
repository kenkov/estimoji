#! /usr/bin/env python
# coding: utf-8

import emoji


def split(text):
    """文を連続する句点と絵文字の箇所で区切る。
    絵文字が入っている場合は付与されている絵文字を返す

    例:

        >>> text = "ありがとう。🙏そのうち行こうか😊"
        >>> split(text)
    """
    chars = []
    emojis = []
    sent_emoji = []

    for c in text:
        if c in {"。"}:
            pass
        elif c in emoji.UNICODE_EMOJI:
                emojis.append(c)
        else:
            if emojis and chars:
                sent_emoji.append(("".join(chars), set(emojis)))
                chars = []
                emojis = []
            chars.append(c)

    return dict(sent_emoji)


if __name__ == "__main__":
    import sys
    import pickle
    import pandas as pd
    from sklearn.utils import Bunch

    items = []

    for line in sys.stdin:
        text = line.strip("\n")
        split_items = split(text)
        for sent, emoji_set in split_items.items():
            for emoji_ in emoji_set:
                items.append((emoji_, emoji.UNICODE_EMOJI[emoji_], sent))

    # データフレームを作成
    frame = pd.DataFrame(items, columns=["emoji", "name", "sent"])

    # 使用する絵文字を頻度上位50件に制限する
    emojis = frame["emoji"].value_counts()
    selected_emojis = emojis.head(50).index
    print("Emoji size: {}, after selecting: {}".format(emojis.shape[0], selected_emojis.shape[0]))
    print("Selected emoji: {}".format(selected_emojis))

    # 絵文字の頻度データをファイルにダンプ
    print("Saving emoji frequency data ...")
    emojis.to_csv("emoji.stats.txt", sep="\t")
    print("Saving emoji frequency data ... done")

    # 選択した絵文字のデータに制限
    selected_frame = frame[frame["emoji"].isin(selected_emojis)]
    print("Data size: {}, after filtering: {}".format(frame.shape[0], selected_frame.shape[0]))

    # これ以降 frame は使用しないので削除
    del frame

    # 正解ラベルを生成
    names = list(sorted(selected_frame["name"].unique()))
    selected_frame["label"] = selected_frame["name"].map({name: i for i, name in enumerate(names)})
    print("Saving data ...")
    selected_frame.to_csv("test.csv")
    print("Saving data ... done")

    # データセットを作成
    dataset = Bunch(data=selected_frame["sent"],
                    target=selected_frame["label"],
                    feature_names=["sent"],
                    target_names=names)

    print("Saving dataset ...")
    pickle.dump(dataset, open("dataset.pkl", "wb"))
    print("Saving dataset ... done")