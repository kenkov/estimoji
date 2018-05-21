#! /usr/bin/env python
# coding: utf-8


import emoji
import os


class Tokenizer:
    def tokenize(self, text):
            return text.split(" ")


def load_emoji_id():
    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            "emoji_id.txt")
    emoji_id = dict()
    with open(filename) as f:
        for i, line in enumerate(f):
            emoji = line.strip("\n")
            emoji_id[emoji] = i
        return emoji_id


def extract_emoji(text):
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