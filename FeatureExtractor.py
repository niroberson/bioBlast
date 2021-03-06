__author__ = 'nathan'
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
import heapq
import dill as pickle


class FeatureExtractor(object):
    def __init__(self):
        self.corpus = None
        self.tfs = None
        self.tfidf = None
        self.cosine_matrix = []
        self.results = []

    @staticmethod
    def tokenize(text):
        tokens = nltk.word_tokenize(text)
        stemmer = PorterStemmer()
        stemmed = []
        for item in tokens:
            stemmed.append(stemmer.stem(item))
        return stemmed

    # This is the vectorizer with are working with that currently uses unigrams and bigrams
    def initialize_vector(self):
        tfidf = TfidfVectorizer(
            ngram_range=(6, 6),
            stop_words='english',
            lowercase=True,
            strip_accents='ascii',
            decode_error='ignore',
            tokenizer=FeatureExtractor.tokenize
        )
        return tfidf

    # Train a vectorizers and save resulting vectorizer in object
    def train(self, corpus, save=True):
        vec = self.initialize_vector()
        tfs = vec.fit_transform(corpus)
        print 'Vectorizer has been trained with', len(vec.vocabulary_.keys()), 'ngrams'
        if save:
            pickle.dump(vec, open('trained_vector.dill', 'wb'))
        self.tfidf = vec
        return tfs

    def load_vector(self):
        self.tfidf = pickle.load(open('trained_vector.dill', 'rb'))

    # Test a corpus with the saved vectorizer
    def test(self, corpus):
        tfs = self.tfidf.transform(corpus)
        return tfs

    # Compute the cosine matrix on a full tfs matrix
    @staticmethod
    def compute_cosine(tfs):
        similarity = tfs.dot(tfs.T).todense()
        return similarity

    # computes the most similar documents to a single entry
    @staticmethod
    def compute_cosine_single(tfs_matrix, tfs_vector):
        similarity = tfs_vector.dot(tfs_matrix.T).todense()
        return similarity



