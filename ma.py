#!/usr/local/anaconda3/bin/python
# -*- coding:utf-8 -*-
import sys
import MeCab
import codecs
import re

STOPWORDS = ["。", ".", ".", "、", ",", "，"]
SKIP_WORD_CLASSES = ["BOS/EOS", "助動詞", "助詞", "代名詞"]

class MA:
    def __init__(self):
        self.mecab = MeCab.Tagger("-Ochasen -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")
        self.stopwords = STOPWORDS
        self.skip_word_classes  = SKIP_WORD_CLASSES
        
    def parse(self, sentence):
        sentence = sentence.strip()
        sentence = re.sub("\u3000", " ", sentence)
        node = self.mecab.parseToNode(sentence)
        res = []
        while node:
            cat1 = node.feature.split(",")[0]
            if node.surface in STOPWORDS:
                node = node.next
                continue
            if cat1 in SKIP_WORD_CLASSES:
                node = node.next
                continue
            res.append(node.surface)
            node = node.next
        return " ".join(res)

if __name__ == '__main__':
    ma = MA()
    with codecs.open("/var/pti/scrape/1.txt", "r", "utf-8") as f:
        for line in f:
            line = line.rstrip()
            x = ma.parse(line)
            print(x)
