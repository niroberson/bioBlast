__author__ = 'nathan'
import MySQLdb as db
import pickle
from FeatureExtractor import FeatureExtractor
import sys
from pymongo import MongoClient

class Medline(object):
    def __init__(self):
        self.con = None
        self.pmids = None
        self.fe = FeatureExtractor()
        self.tfs_dict = None
        self.mongodb = None
        self.mapOfAbstracts = dict()

    def connect_mysql(self, DEBUG=False):
        # Setup connection to etblast mysql databse
        if DEBUG:
            HOST = "localhost"
            USER = "johnny"
            PASSWORD = "johnny"
            DB = "etblast"
        else: # Deployed on server
            HOST = 'localhost'
            USER = "johnny"
            PASSWORD = "johnny"
            DB = "etblast"
        self.con = db.connect(host=HOST, user=USER, passwd=PASSWORD, db=DB)

    def connect_mongo(self, DEBUG=False):
        client = MongoClient()
        if DEBUG:
            test = client.test
            return test
        else:
            self.mongodb = client.bioBlast

    def insert_tfs_mongo(self):
        collection = self.mongodb.tfs_matrix
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT PMID, AbstractText FROM MEDLINE_0 LIMIT 20000;")
            rows = cur.fetchall()
            for i, row in enumerate(rows):
                if row[1] is not None & collection.find_one({"pmid": row[0]}) is None:
                    tfs_entry = self.fe.vectorize_corpus([row[1]])
                    post = {
                        "pmid": row[0],
                        "tfs_vector": tfs_entry
                    }
                    collection.insert_one(post).inserted_id

    def insert_tfs_mysql(self):
           with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT PMID, AbstractText FROM MEDLINE_0 LIMIT 20000;")
            rows = cur.fetchall()
            cur2 = self.con.cursor()
            for i, row in enumerate(rows):
                cur2.execute("SELECT * FROM bioBlast WHERE PMID=" + row[0])
                entry = cur2.fetchone()
                if row[1] is not None:
                    if entry is None: # if not in mysql table, add to table
                        add_entry = ("INSERT INTO bioBlast "
                        "(pmid, tfs_vector) "
                        "VALUES (%s, %s)")
                        pickled_abstract = pickle.dumps(self.fe.vectorize_corpus([row[1]]))
                        entry_data = (row[0], pickled_abstract)
                        cur2.execute(add_entry, entry_data)

    def train_vocabulary(self):
        with self.con:
            cur = self.con.cursor()
            n_articles = "200000"
            cur.execute("SELECT PMID, AbstractText FROM MEDLINE_0 LIMIT " + n_articles + ";")
            for i in range(cur.rowcount):
                row = cur.fetchone()
                if row[1]:
                    self.mapOfAbstracts[row[0]] = row[1]
        extracted_corpus = self.fe.extract_corpus(self.mapOfAbstracts.values())
        tfs = self.fe.vectorize_corpus(extracted_corpus)


