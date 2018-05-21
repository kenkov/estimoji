# estimoji

文の末尾に付与する絵文字を推定するライブラリです。

## インストール

Python 3.6.0 で動作確認しています。対応のPythonをインストール後、依存ライブラリをインストールしてください。

日本語での学習データ作成の際には MeCab 等を用いて文を単語で区切る必要があります。

## 学習データの作成

    echo "ありがとう。🙏そのうち行こうか😊" | mecab -O wakati | python -m estimoji.generate_dataset --out dataset.pkl

## 学習