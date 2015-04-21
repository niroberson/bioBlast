from unittest import TestCase
from FeatureExtractor import FeatureExtractor

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
        self.feature_extractor.vectorize_corpus(extracted)
        self.feature_extractor.compute_cosine(self.feature_extractor.tfs)
        self.assertEqual(36, len(self.feature_extractor.cosine_matrix))

    def test_get_n_top_matches(self):
        extracted = self.feature_extractor.extract_corpus(data)
        self.feature_extractor.vectorize_corpus(extracted)
        self.feature_extractor.compute_cosine(self.feature_extractor.tfs)
        self.feature_extractor.find_matches(self.feature_extractor.cosine_matrix, self.feature_extractor.corpus)
        self.assertEqual(self.feature_extractor.results[0][0], self.feature_extractor.results[0][1])
        self.assertEqual(len(data) ** 2, len(self.feature_extractor.results))
        # for result in self.feature_extractor.results:
        # print self.feature_extractor.cosine_matrix
        #     print result, "\n"

    def test_single_entry(self):
        extracted = self.feature_extractor.extract_entry(data2[0])
        self.feature_extractor.initialize_vectorize()
        self.feature_extractor.fit_transform_entry(extracted)
        cosine_mat = self.feature_extractor.compute_cosine(self.feature_extractor.tfs)
        self.assertAlmostEqual(1, cosine_mat[0])

    def test_multiple_single_entry(self):
        extracted = self.feature_extractor.extract_entry(data2[0])
        print extracted
        self.feature_extractor.initialize_vectorize()
        self.feature_extractor.fit_transform_entry(extracted)

        extracted = self.feature_extractor.extract_entry(data3[0])
        print extracted
        self.feature_extractor.initialize_vectorize()
        self.feature_extractor.fit_transform_entry(extracted)

        cosine_mat = self.feature_extractor.compute_cosine(self.feature_extractor.tfs)
        self.assertEqual(2, cosine_mat.size)