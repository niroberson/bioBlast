__author__ = 'nathan'
from unittest import TestCase
from Medline import Medline
import pickle
import timeit

class TestMedline(TestCase):

    def setUp(self):
        self.m = Medline()

    def test_mysql(self):
        self.m.connect_mysql(True)
        with self.m.mysql:
            x = self.m.mysql.cursor()
            test_vec = [1, 2, 3, 4, 5, 6]
            pickled_vector = pickle.dumps(test_vec)
            x.execute("""INSERT INTO bioBlast VALUES (%s, %s)""", ("12345678", pickled_vector))

    def test_mongodb(self):
        self.m.connect_mongo(True)
        pmid = "123789"
        tfs_vector = "[1 2 3 4 5 6 7 8]"
        self.m.insert_tfs_mongo(pmid, tfs_vector)
        test_entry = self.m.mongo_coll.find_one({"pmid": "123789"})
        self.assertEqual("[1 2 3 4 5 6 7 8]", test_entry["tfs_vector"])
        self.m.mongo_coll.remove({"pmid": "123789"})

    def test_get_tfs(self):
        self.m.connect_mysql(True)
        self.m.connect_mongo(True)
        self.m.train_vocabulary(10000)
        self.m.process_abstracts(100000)
        count = self.m.mongo_coll.count()
        self.assertEqual(1324, count)
        self.m.mysql.close()

    def test_get_tfs_vectors(self):
        self.m.connect_mongo(True)
        pmid_list, tfs_map = self.m.create_tfs_matrix()
        self.assertEqual(1324, len(pmid_list))
        self.assertEqual(1324, len(tfs_map))


    def time_tests(self):
        t = timeit.timeit(self.test_mongodb, number=1)
        print("{:30s} {:f}".format("time mongoDB", t))
        t2 = timeit.timeit(self.test_get_tfs, number=1)
        print("{:30s} {:f}".format("time get_tfs", t2))
