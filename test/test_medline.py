from unittest import TestCase
from Medline import Medline
__author__ = 'nathan'


class TestMedline(TestCase):

    def test_get_pmids(self):
        medline = Medline()
        medline.get_pmids()