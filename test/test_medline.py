from unittest import TestCase
from Medline import Medline
__author__ = 'nathan'
import pickle

class TestMedline(TestCase):

    def setUp(self):
        self.m = Medline()

    def test_mysql(self):
        self.m.connect_mysql(True)
        with self.m.con:
            x = self.m.con.cursor()
            test_vec = [1, 2, 3, 4, 5, 6]
            pickled_vector = pickle.dumps(test_vec)
            x.execute("""INSERT INTO bioBlast VALUES (%s, %s)""", ("12345678", pickled_vector))

    def test_mongodb(self):
        self.m.connect_mongo(True)
        pmid = "123789"
        tfs_vector = "[1 2 3 4 5 6 7 8]"
        self.m.insert_tfs_mongo(pmid, tfs_vector)
        test_entry = self.m.mongodb.find_one({"pmid": "123789"})
        self.assertEqual("[1 2 3 4 5 6 7 8]", test_entry["tfs_vector"])

    def test_insert_tfs(self):
        self.m.connect_mysql(True)
        self.m.insert_tfs_vector("123789", "[1 2 3 7 8 9]")
        cur = self.m.con.cursor()
        record_check = "SELECT (1) FROM bioBlast WHERE pmid = " + "123789" + " LIMIT 1;"
        self.assertTrue(cur.execute(record_check))
        self.m.con.close()

    def test_get_tfs(self):
        self.m.connect_mysql(True)
        self.m.connect_mongo(True)
        self.m.train_vocabulary(10000)
        self.m.get_tfs_vectors(100000)
        count = self.m.coll.count()
        self.assertEquals(1325, count)
        self.m.con.close()

    ### Necessary Tests
        # Test entry exists in database (query database and ensure accurate values)


