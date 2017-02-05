#!/usr/local/anaconda3/bin/python
# -*- coding:utf-8 -*-
import sys
import MeCab
import codecs
import re

STOPWORDS = ["。", ".", ".", "、", ",", "，", "「", "」", "ロイター", "もの", "こと", "ごろ", "なっ", "もっ", "いる", "する", "ある", "なる", "れる", "よう", "その", "いう", "その", "これ", "この", "それ", "ごと", "これ", "ため", "こうした", "られる", "しれ", "ため", "どう", "だれ", "さん", "よる", "である", "ところ", "ゆえ", "ただ"]
#SKIP_WORD_CLASSES = ["BOS/EOS", "助動詞", "助詞", "代名詞", "接続詞"]
WORD_CLASSES = ["名詞"]

class MA:
    def __init__(self):
        self.mecab = MeCab.Tagger("-Ochasen -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")
        self.stopwords = STOPWORDS
        self.word_classes  = WORD_CLASSES
        
    def parse(self, sentence):
        sentence = sentence.strip()
        sentence = sentence.replace("\u3000", " ")
        sentence = sentence.replace("\xa0", " ")
        node = self.mecab.parseToNode(sentence)
        res = []
        while node:
            cat1 = node.feature.split(",")[0]
            if cat1 not in self.word_classes:
                node = node.next
                continue
            if node.surface in self.stopwords:
                node = node.next
                continue           
            res.append(node.surface)
            node = node.next
        return " ".join(res)

if __name__ == '__main__':
    ma = MA()
    print(ma.parse(u"ロイター通信社"))
    with codecs.open("/var/pti/scrape/1.txt", "r", "utf-8") as f:
        for line in f:
            line = line.rstrip()
            x = ma.parse(line)
            print(x)
