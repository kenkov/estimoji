# estimoji

文の末尾に付与する絵文字を推定するライブラリです。

## インストール

Python 3.6.0 で動作確認しています。対応のPythonをインストール後、本ライブラリと依存ライブラリをインストールしてください。

    $ pip install git+https://github.com/kenkov/estimoji

日本語での学習データ作成の際には MeCab 等を用いて文を単語で区切る必要があります。

## 使い方

### 学習データの作成

    $ echo "ありがとう。🙏そのうち行こうか😊" | mecab -O wakati | python -m estimoji.transform --out dataset.pkl --csv dataset.csv
    Data size: 2, after filtering: 2
    Saving data in dataset.csv ...
    Saving data in dataset.csv ... done
    Saving dataset in dataset.pkl ...
    Saving dataset in dataset.pkl ... done
    $ cat dataset.csv
    ,emoji,label,sent
    0,🙏,10,ありがとう
    1,😊,5, そのうち 行こ う か

### 学習

    $ python -m estimoji.fit --dataset dataset.pkl --out model.pkl

### 推論

入力した文の文末に付与されそうな絵文字を確率付きで上位 5 つ出力します。

    $ echo "絵文字を推定します！" | mecab -Owakati | python -m estimoji.predict --model baseline/model.pkl
    0.2140 😊
    0.2106 🐰
    0.0721 😔
    0.0687 💖
    0.0615 🙂

