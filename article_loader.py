#!/usr/local/anaconda3/bin/python
# -*- coding:utf-8 -*-

from ma import MA
import os
import codecs

class ArticleLoader:
    def __init__(self):
        self.ma = MA()

    def load_article(self, filename):
        article = []
        with codecs.open(filename, "r", "utf-8") as f:
            for line in f:
                line = line.strip()
                article.append(self.ma.parse(line))

        return " ".join(article)

    def load_articles(self, dirname):
        doc2idx = []
        articles = []
        for basename in os.listdir(dirname):
            filepath = os.path.join(dirname, basename)
            if not filepath.endswith(".txt"):
                continue

            article = self.load_article(filepath)
            if article is not None:
                doc2idx.append(basename.rstrip(".txt"))
                articles.append(article)

        return (doc2idx, articles)

if __name__ == '__main__':
    ldr = ArticleLoader()
    ldr.load_articles("/var/pti/scrape")
