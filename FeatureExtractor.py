__author__ = 'nathan'
from sklearn.externals import joblib
import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
import heapq


class FeatureExtractor(object):
    def __init__(self):
        self.corpus = None
        self.tfs = None
        self.tfidf = None
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
        extracted_corpus = []
        for entry in corpus:
            if entry:
                extracted_corpus.append(self.extract_entry(entry))
        return extracted_corpus

    @staticmethod
    def extract_entry(entry):
        lowers = entry.lower()
        no_punctuation = lowers.translate(None, string.punctuation)
        extracted = no_punctuation
        return extracted

    # This is the vectorizer with are working with that currently uses unigrams and bigrams
    def initialize_vector(self):
        tfidf = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words='english',
            lowercase=True,
            strip_accents='ascii',
            decode_error='ignore'
        )
        return tfidf

    # Train a vectorizers and save resulting vectorizer in object
    def train(self, corpus, save=True):
        vec = self.initialize_vector()
        extracted_corpus = self.extract_corpus(corpus)
        tfs = vec.fit_transform(extracted_corpus)
        print 'Vectorizer has been trained with', len(vec.vocabulary_.keys()), 'words'
        if save:
            joblib.dump(vec, 'trained_vector.joblib')
        self.tfidf = vec
        return tfs

    def load_vector(self):
        self.tfidf = joblib.load('trained_vector.joblib')

    # Test a corpus with the saved vectorizer
    def test(self, corpus):
        extracted_corpus = self.extract_corpus(corpus)
        tfs = self.tfidf.transform(extracted_corpus)
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
        extracted_corpus = self.extract_corpus(corpus)
        tfs = self.train(extracted_corpus)
        cosine_matrix = self.compute_cosine
        cosine_matrix = list(cosine_matrix.flat)
        sorted_matches = heapq.nlargest(len(cosine_matrix), range(len(cosine_matrix)), key=cosine_matrix.__getitem__)
        for j in sorted_matches:
            row = j / len(corpus)
            column = j % len(corpus)
            self.results.append([corpus[row], corpus[column], cosine_matrix[j]])
        return self.results



