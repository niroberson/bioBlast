__author__ = 'nathan'


from Medline import Medline

m = Medline()
#
m.connect()
# # m.get_pmids()
# m.get_abstracts()
m.extract_corpus()

from FeatureExtractor import FeatureExtractor

fe = FeatureExtractor()


