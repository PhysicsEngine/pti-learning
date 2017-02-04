from __future__ import print_function

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation

import pickle

class PTILDA:

    n_features = 1000
    n_topics = 2

    tfv_file = "tfv.pkl"
    tf_file = "tf.pkl"
    model_file = "lda.pkl"

    def __init__(self):
        pass

    def train(self, dataset):
        # Use tf (raw term count) features for LDA.
        self.tf_vectorizer = CountVectorizer(max_df=0.95, min_df=1,
                                max_features=self.n_features)
        self.tf = self.tf_vectorizer.fit_transform(dataset)

        # Train Model
        self.lda = LatentDirichletAllocation(n_topics=self.n_topics, max_iter=5,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)
        self.lda.fit(self.tf)

        # predict data
        self.matrix = self.lda.transform(self.tf)

        # save model
        pickle.dump(self.tf_vectorizer, open(self.tfv_file, "wb"))
        pickle.dump(self.tf, open(self.tf_file, "wb"))
        pickle.dump(self.lda, open(self.model_file, "wb"))

    def load(self):
        self.tf_vectorizer = pickle.load(open(self.tf_vectorizer, "rb"))
        self.tf = pickle.load(open(self.tf_file, "rb"))
        self.lda = pickle.load(open(self.model_file, "rb"))
        self.matrix = self.lda.transform(self.tf)

    def print_topic_word(self, n_top_words, topic_num=None):
        feature_names = self.tf_vectorizer.get_feature_names()
        for topic_idx, topic in enumerate(self.lda.components_):
            if topic_num is None or topic_num == topic_idx:
                print("Topic #{}:".format(topic_idx))
                print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
            print()

    def print_doc_topic(self, n_top, doc_id=None):
        for i, doc in enumerate(self.matrix):
            if doc_id is None or i == doc_id:
                print("Doc {}:".format(i))
                topics = {}
                for topic_num, prob in enumerate(doc):
                    topics[topic_num] = prob
                count = 0
                for k, v  in sorted(topics.items(), key=lambda x:x[1], reverse=True):
                    print ("Topic:{}, prob:{}".format(k, v))
                    count += 1
                    if count >= n_top:
                        break
                print()

    def dump_topic(self, idx2doc):
        for i, doc in enumerate(self.matrix):
            result = []
            for j, x in enumerate(doc):
                result.append((j, x))
                pickle.dump(result, open("/var/pti/topic/{}.pkl".format(idx2doc[i]), "wb"))
