from unittest import TestCase
from FeatureExtractor import FeatureExtractor
import timeit
import numpy as np

__author__ = 'nathan'

data = ["All of my brother's sons are in college",
        "My brother went to the grocery store to buy milk",
        "Milk comes from cows",
        "My brother owns a cow and takes it to his son's college",
        "Spider cows are in the news very often",
        "My brother's son's college is nearby"]
data2 = ("All of my brother's daughters are in preschool",)
data3 = ("When will it be time for lunch?",)

class TestFeatureExtractor(TestCase):
    def setUp(self):
        self.feature_extractor = FeatureExtractor()

    def test_tokenize(self):
        a = "realized realizes realization"
        stemmed = self.feature_extractor.tokenize(a)
        for stem in stemmed:
            self.assertEqual("realiz", stem)

    def test_extract_corpus(self):
        extracted = self.feature_extractor.extract_corpus(data)
        self.assertEqual(6, len(extracted))

    def test_compute_cosine(self):
        extracted = self.feature_extractor.extract_corpus(data)
        tfs = self.feature_extractor.train(extracted)
        cosine_matrix = self.feature_extractor.compute_cosine(tfs)
        self.assertEqual(6, len(cosine_matrix))
        self.assertAlmostEqual(1, cosine_matrix[0,0])

    def test_get_n_top_matches(self):
        results = self.feature_extractor.find_matches(data)
        self.assertEqual(results[0][0], results[0][1])
        self.assertEqual(len(data) ** 2, len(results))

    def test_compute_single_cosine(self):
        # Test the response is the identity vector
        tfs_matrix = self.feature_extractor.train(data)
        extracted_entry = self.feature_extractor.extract_entry(data[0])
        tfs_vector = self.feature_extractor.tfidf.transform([extracted_entry])
        cosine = self.feature_extractor.compute_cosine_single(tfs_matrix, tfs_vector)
        self.assertAlmostEquals(1, cosine[0, 0])

    def time_tests(self):
        t3 = timeit.timeit(self.test_compute_single_cosine, number=1)
        print("{:30s} {:f}".format("time single_cosineB", t3))
        t2 = timeit.timeit(self.test_compute_cosine_ngram, number=1)
        print("{:30s} {:f}".format("time full cosine", t2))

    def test_load_vector(self):
        self.feature_extractor.train(data)
        self.feature_extractor.load_vector()
        results = self.feature_extractor.test(data)
        self.assertEquals(6, len(results.todense()))
