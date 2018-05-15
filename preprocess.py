#! /usr/bin/env python
# coding: utf-8


import re
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
    from collections import Counter
    import pandas as pd

    items = []

    for line in sys.stdin:
        text = line.strip("\n")
        split_items = split(text)
        for sent, emoji_set in split_items.items():
            for emoji_ in emoji_set:
                items.append((emoji_, emoji.UNICODE_EMOJI[emoji_], sent))

    frame = pd.DataFrame(items, columns=["emoji", "name", "sent"])
    frame.to_csv("test.csv")