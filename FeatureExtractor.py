__author__ = 'nathan'
import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import linear_kernel
from numpy import hstack
import numpy
import heapq
import cPickle as pickle


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

    def vectorize_corpus(self, extracted_corpus):
        if self.tfidf is None:
            tfidf = TfidfVectorizer(
                tokenizer=self.tokenize,
                stop_words='english',
            )
            tfs = tfidf.fit_transform(extracted_corpus)
            self.tfidf = tfidf
            print 'Vectorizer has been trained with', len(tfidf.vocabulary_.keys()), 'words'
            self.save_tfidf_os(self.tfidf)
        else:
            tfidf = self.tfidf
            tfs = tfidf.fit_transform(extracted_corpus)
        return tfs

    @staticmethod
    def save_tfidf_os(tfidf):
        # Save vocabulary used in training
        pickle.dump(tfidf.vocabulary_, open("trained_tfidf.p", "wb"))

    def load_tfidf_os(self):
        vocab_dict = pickle.load(open("trained_tfidf.p", "rb"))
        self.tfidf = TfidfVectorizer(
            tokenizer=self.tokenize,
            stop_words='english',
            vocabulary=vocab_dict
        )

    def compute_cosine(self, tfs):
        similarity = tfs.dot(tfs.T).todense()
        return similarity

    def compute_cosine_single(self, tfs_matrix, tfs_vector):
        similarity = tfs_vector.dot(tfs_matrix.T).todense()
        return similarity

    def find_matches(self, corpus):
        extracted_corpus = self.extract_corpus(corpus)
        tfs = self.vectorize_corpus(extracted_corpus)
        cosine_matrix = self.compute_cosine(tfs)
        cosine_matrix = list(cosine_matrix.flat)
        sorted_matches = heapq.nlargest(len(cosine_matrix), range(len(cosine_matrix)), key=cosine_matrix.__getitem__)
        for j in sorted_matches:
            row = j / len(corpus)
            column = j % len(corpus)
            self.results.append([corpus[row], corpus[column], cosine_matrix[j]])
        return self.results

    def ngram_vectorizerA(self, corpus):
        tfidf = TfidfVectorizer(
            tokenizer=self.tokenize,
            ngram_range=(2, 5),
            stop_words='english',
            lowercase=True,
            strip_accents='ascii',
            decode_error='ignore'
        )
        tfs = tfidf.fit_transform(corpus)
        self.tfidf = tfidf
        return tfs

    def ngram_vectorizerB(self, corpus):
        tfidf = TfidfVectorizer(
            tokenizer=self.tokenize,
            ngram_range=(1, 5),
            stop_words='english',
            lowercase=True,
            strip_accents='ascii',
            decode_error='ignore'
        )
        tfs = tfidf.fit_transform(corpus)
        self.tfidf = tfidf
        return tfs


