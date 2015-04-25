__author__ = 'nathan'


from Medline import Medline
from Article import Article

m = Medline()
#
m.connect()
# m.get_pmids()
m.get_abstracts()

