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
        extracted = []
        for entry in corpus:
            lowers = entry.lower()
            no_punctuation = lowers.translate(None, string.punctuation)
            extracted.append(no_punctuation)
        return extracted

    def vectorize_corpus(self, extracted):
        tfidf = TfidfVectorizer(tokenizer=self.tokenize, stop_words='english')
        self.tfs = tfidf.fit_transform(extracted)

    def compute_cosine(self, tfs):
        for i, row in enumerate(tfs):
            self.cosine_matrix = hstack((self.cosine_matrix, linear_kernel(row, tfs).flatten()))

    def find_matches(self, cosine_matrix, corpus):
        sorted_matches = heapq.nlargest(len(cosine_matrix), range(len(cosine_matrix)), key=cosine_matrix.__getitem__)
        for j in sorted_matches:
            row = j / len(corpus)
            column = j % len(corpus)
            self.results.append([corpus[row], corpus[column], cosine_matrix[j]])