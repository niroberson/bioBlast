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
            tfidf = TfidfVectorizer(tokenizer=self.tokenize, stop_words='english')
            tfs = tfidf.fit_transform(extracted_corpus)
            self.tfidf = tfidf
            print 'Vectorizer has been trained with', len(tfidf.vocabulary_.keys()), 'words'
        else:
            tfidf = self.tfidf
            tfs = tfidf.transform(extracted_corpus)
        return tfs

    def compute_cosine(self, tfs):
        for i, row in enumerate(tfs):
            self.cosine_matrix = hstack((self.cosine_matrix, linear_kernel(row, tfs).flatten()))
        return self.cosine_matrix

    def find_matches(self, corpus):
        extracted_corpus = self.extract_corpus(corpus)
        tfs = self.vectorize_corpus(extracted_corpus)
        cosine_matrix = self.compute_cosine(tfs)
        sorted_matches = heapq.nlargest(len(cosine_matrix), range(len(cosine_matrix)), key=cosine_matrix.__getitem__)
        for j in sorted_matches:
            row = j / len(corpus)
            column = j % len(corpus)
            self.results.append([corpus[row], corpus[column], cosine_matrix[j]])
        return self.results