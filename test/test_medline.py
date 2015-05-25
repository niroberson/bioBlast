__author__ = 'nathan'
from unittest import TestCase
from Medline import Medline
import timeit

class TestMedline(TestCase):

    def setUp(self):
        self.m = Medline()

    def test_get_tfs(self):
        self.m.connect_mysql(True)
        self.m.connect_mongo(True)
        self.m.train_vocabulary(10000)
        self.m.process_abstracts(self.m.mysql, start=0, limit=10000)
        count = self.m.mongo_coll.count()
        self.assertEqual(5644, count)

    def test_get_tfs_vectors(self):
        self.m.connect_mongo(True)
        tfs_map = self.m.create_tfs_map()
        self.assertEqual(2, len(tfs_map))

    def time_tests(self):
        t2 = timeit.timeit(self.test_get_tfs, number=1)
        print("{:30s} {:f}".format("time get_tfs", t2))
        t = timeit.timeit(self.test_similarity_from_load, number=1)
        print("{:30s} {:f}".format("time get_tfs", t))

    def test_multiprocess_abstracts(self):
        self.m.connect_mongo(True)
        self.m.connect_mysql(True)
        self.m.train_vocabulary(10000)
        self.m.queue_process(0, 120000)

    def test_count_rows(self):
        self.m.connect_mysql(True)
        cur = self.m.mysql.cursor()
        cur.execute("SELECT COUNT(*) FROM MEDLINE_0;")
        res = cur.fetchone()
        print res[0]
        self.assertEquals(23343329, res[0])

    def test_similarity_from_load(self):
        self.m.connect_mongo(True)
        tfs_matrix, pmid_array = self.m.create_tfs_map()
        similarity = self.m.tfs_matrix_similarity(tfs_matrix)
        self.assertEquals(5645, len(pmid_array))
        self.assertEquals(5645, similarity.shape[0])
        self.assertAlmostEquals(1, similarity[1, 1])