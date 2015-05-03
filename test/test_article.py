from unittest import TestCase
from Article import Article
__author__ = 'nathan'


class TestArticle(TestCase):
    def test_fill_fields(self):
        article = Article('25896973')
        article.fill_all_fields()
        self.assertEquals("25896973", article.pmid)
        self.assertEquals("2015 May 1", article.date)
        self.assertEqual("Clinical cancer research : an official journal of the American Association for Cancer Research", article.journal)





