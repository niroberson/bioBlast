__author__ = 'nathan'
import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import linear_kernel
from numpy import hstack
import heapq

class FeatureExtractor(object):
    def __init__(self):
        self.corpus = None
        self.extracted_corpus = []
        self.tfs = None
        self.cosine_matrix = []
        self.results = []

    @staticmethod
    def stem_tokens(tokens):
        stemmer = PorterStemmer()
        stemmed = []
        for item in tokens:
            stemmed.append(stemmer.stem(item))
        return stemmed

    def tokenize(self, text):
        tokens = nltk.word_tokenize(text)
        stems = self.stem_tokens(tokens)
        return stems

    def extract_corpus(self, corpus):
        self.corpus = corpus
        for entry in corpus:
            lowers = entry.lower()
            no_punctuation = lowers.translate(None, string.punctuation)
            self.extracted_corpus.append(no_punctuation)

    def vectorize_corpus(self):
        tfidf = TfidfVectorizer(tokenizer=self.tokenize, stop_words='english')
        self.tfs = tfidf.fit_transform(self.extracted_corpus)

    def compute_cosine(self):
        for row in self.tfs:
            self.cosine_matrix = hstack((self.cosine_matrix, linear_kernel(row, self.tfs).flatten()))

    def get_n_top_matches(self, n):
        top_matches = heapq.nlargest(n, range(len(self.cosine_matrix)), key=self.cosine_matrix.__getitem__)
        for j in top_matches:
            row = j / len(self.corpus)
            column = j % len(self.corpus)
            self.results.append([self.corpus[row], self.corpus[column], self.cosine_matrix[j]])
