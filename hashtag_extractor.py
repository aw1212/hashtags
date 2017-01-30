import os.path
import string
from collections import Counter

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize

from hashtag import Hashtag
from database.data_storage import *
from database.database_connection import get_initialized_database_connection

PATH = 'c:/Users/Alessandra/Downloads/eigen/test docs/'
FILE = 'doc1.txt'
TOP_N = 10
data = []


def get_most_common_tokens(tokens):
    cnt = Counter()
    for token in tokens:
        cnt[token] += 1
    common_tokens = [t for t, _ in cnt.most_common(TOP_N)]
    print('TOP %s MOST COMMON WORDS: %s'%(TOP_N, common_tokens))
    return common_tokens


def add_tokens_to_list(sentence, filename, common_tokens):
    common_words = []
    for token in common_tokens:
        word = " " + token.lower() + " "
        phrase = " " + sentence.lower() + " "
        if word in phrase:
            common_words.append(token)
    for common_word in common_words:
        hashtag = Hashtag(filename, common_word, sentence)
        data.append(hashtag)


def get_hastags():
    filepath = os.path.normpath(PATH + FILE)
    with open(filepath) as f:
        text = f.read()
        tokens = text.split()
        stopwords_removed = [i.lower() for i in tokens if i.lower() not in stopwords.words('english')]
        filtered_tokens = [i.lower() for i in stopwords_removed if i.lower() not in string.punctuation]
        top_n_common_tokens = get_most_common_tokens(filtered_tokens)
        for sent in sent_tokenize(text):
            if any(word.lower() in sent.lower() for word in top_n_common_tokens):
                add_tokens_to_list(sent, FILE, top_n_common_tokens)


if __name__ == '__main__':
    connection = get_initialized_database_connection()
    get_hastags()
    for hashtag in data:
        save_hashtag(hashtag, connection)
    print_contents_of_table(connection)
    connection.close()