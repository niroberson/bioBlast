__author__ = 'nathan'
from unittest import TestCase
from Medline import Medline
import pickle
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
        self.assertEqual(1329, count)

    def test_get_tfs_vectors(self):
        self.m.connect_mongo(True)
        pmid_list, tfs_map = self.m.create_tfs_matrix()
        self.assertEqual(1329, len(pmid_list))
        self.assertEqual(1329, len(tfs_map))

    def time_tests(self):
        t = timeit.timeit(self.test_mongodb, number=1)
        print("{:30s} {:f}".format("time mongoDB", t))
        t2 = timeit.timeit(self.test_get_tfs, number=1)
        print("{:30s} {:f}".format("time get_tfs", t2))

    def test_multiprocess_abstracts(self):
        self.m.connect_mongo(True)
        self.m.connect_mysql(True)
        self.m.train_vocabulary(10000)
        self.m.queue_process(120000)

    def test_count_rows(self):
        self.m.connect_mysql(True)
        cur = self.m.mysql.cursor()
        cur.execute("SELECT COUNT(*) FROM MEDLINE_0;")
        res = cur.fetchone()
        print res[0]
        self.assertEquals(23343329, res[0])