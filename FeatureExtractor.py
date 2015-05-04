__author__ = 'nathan'
import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
import heapq
import scipy.spatial.distance

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

    # Train a vectorizers and save resulting vectorizer in objcet
    def train(self, corpus):
        self.ngram_vectorizerA(corpus)
        print 'Vectorizer has been trained with', len(self.tfidf.vocabulary_.keys()), 'words'

    # Test a corpus with the saved vectorizer
    def test(self, corpus):
        tfs = self.tfidf.transform(corpus)
        return tfs

    # Train and vectorizer and result the resulting tfs matrix
    def test_train(self, corpus):
        tfs = self.ngram_vectorizerA(corpus)
        return tfs

    # Compute the cosine matrix on a full tfs matrix
    def compute_cosine(self, tfs):
        similarity = tfs.dot(tfs.T).todense()
        return similarity

    # Return the cosine vector for a single entry
    def compute_cosine_singleA(self, tfs_matrix, tfs_vector):
        vector = tfs_vector.todense()
        return scipy.spatial.distance.cdist(tfs_matrix.todense(), vector, 'cosine')

    def compute_cosine_singleB(self, tfs_matrix, tfs_vector):
        similarity = tfs_vector.dot(tfs_matrix.T).todense()
        return similarity

    # Stub to find matches from cosine matrix. This will need to be changed once a cosine matrix is created
    def find_matches(self, corpus):
        extracted_corpus = self.extract_corpus(corpus)
        tfs = self.test_train(extracted_corpus)
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


