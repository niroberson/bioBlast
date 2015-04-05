from unittest import TestCase
from FeatureExtractor import FeatureExtractor

__author__ = 'nathan'

data = ["All of my brother's sons are in college",
        "My brother went to the grocery store to buy milk",
        "Milk comes from cows",
        "My brother owns a cow and takes it to his son's college",
        "Spider cows are in the news very often",
        "My brother's son's college is nearby"]


class TestFeatureExtractor(TestCase):
    def setUp(self):
        self.feature_extractor = FeatureExtractor()

    def test_stem_tokens(self):
        a = ["realized", "realizes", "realization"]
        stemmed = self.feature_extractor.stem_tokens(a)
        for stem in stemmed:
            self.assertEqual("realiz", stem)

    def test_tokenize(self):
        a = "realized realizes realization"
        stemmed = self.feature_extractor.tokenize(a)
        for stem in stemmed:
            self.assertEqual("realiz", stem)

    def test_extract_corpus(self):
        self.feature_extractor.extract_corpus(data)
        self.assertEqual(6, len(self.feature_extractor.extracted_corpus))

    def test_compute_cosine(self):
        self.feature_extractor.extract_corpus(data)
        self.feature_extractor.vectorize_corpus()
        self.feature_extractor.compute_cosine()
        self.assertEqual(36, len(self.feature_extractor.cosine_matrix))

    def test_get_n_top_matches(self):
        self.feature_extractor.extract_corpus(data)
        self.feature_extractor.vectorize_corpus()
        self.feature_extractor.compute_cosine()
        results = self.feature_extractor.get_n_top_matches(8)
        self.assertEqual(results[0][0], results[0][1])
        for result in results:
            print result, "\n"