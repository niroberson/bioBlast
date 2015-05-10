__author__ = 'nathan'
from sklearn.externals import joblib
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
            ngram_range=(1, 2),
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
        print 'Vectorizer has been trained with', len(vec.vocabulary_.keys()), 'words'
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

    # Stub to find matches from cosine matrix. This will need to be changed once a cosine matrix is created
    def find_matches(self, corpus):
        tfs = self.train(corpus)
        cosine_matrix = self.compute_cosine(tfs)
        cosine_matrix = list(cosine_matrix.flat)
        sorted_matches = heapq.nlargest(len(cosine_matrix), range(len(cosine_matrix)), key=cosine_matrix.__getitem__)
        for j in sorted_matches:
            row = j / len(corpus)
            column = j % len(corpus)
            self.results.append([corpus[row], corpus[column], cosine_matrix[j]])
        return self.results



