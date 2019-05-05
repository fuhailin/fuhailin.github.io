#! python3
# -*- coding: utf-8 -*-

import nltk
import ssl
import math
import string

from nltk.corpus import stopwords
from collections import Counter
from nltk.stem.porter import*

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download()

nltk.download('punkt')
nltk.download('stopwords')

text1 = "I heard about Spark and I love Spark"

text2 = "I wish Java could use case classes'"

text3 = "Logistic regression models are neat"


def get_tokens(text):
    lower = text.lower()
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    no_punctuation = lower.translate(remove_punctuation_map)
    tokens = nltk.word_tokenize(no_punctuation)

    return tokens


def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))

    return stemmed


def tf(word, count):
    tfv = count[word] / sum(count.values())
    return tfv


def n_containing(word, count_list):
    df = sum(1 for count in count_list if word in count)
    return df


def idf(word, count_list):
    idfv = math.log(len(count_list) / (1 + n_containing(word, count_list)))
    return idfv


def tfidf(word, count, count_list):
    return tf(word, count) * idf(word, count_list)


def count_term(text):
    tokens = get_tokens(text)
    filtered = [w for w in tokens if not w in stopwords.words('english')]  # remove stopwords
    stemmer = PorterStemmer()
    stemmed = stem_tokens(filtered, stemmer)
    count = Counter(stemmed)
    return count


def main():
    texts = [text1, text2, text3]
    countlist = []
    for text in texts:
        countlist.append(count_term(text))
    for i, count in enumerate(countlist):
        print("Top words in document {}".format(i + 1))
        scores = {word: tfidf(word, count, countlist) for word in count}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        for word, score in sorted_words[:5]:
            print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))


if __name__ == "__main__":
    main()
