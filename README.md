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


### コードからの利用

`estimoji.model.load_model` で scikit-learn の Estimator をロードして使います。

    >>> from estimoji.model import load_model
    >>> model = load_model("baseline/model.pk")
    >>> text = "絵文字 を 推定 し ます"
    >>> model.predict([text])
    array(['😊'], dtype=object)
    >>> list(zip(model.classes_, model.predict_proba([text])[0]))[:5]
    [('☔', 8.2845765559201167e-05),
     ('☹', 1.978231655166077e-06),
     ('☺', 0.00051007152524201315),
     ('♥', 0.0010444626623881271),
     ('✊', 0.00017314542464209174)]
