__author__ = 'nathan'
import MySQLdb as db
import pickle
from FeatureExtractor import FeatureExtractor
import sys
from pymongo import MongoClient

class Medline(object):
    def __init__(self):
        self.MapOfAbstracts = dict()
        self.con = None
        self.pmids = None
        self.fe = FeatureExtractor()
        self.tfs_dict = None
        self.mongodb = None

    def connect_mysql(self, DEBUG=False):
        # Setup connection to etblast mysql databse
        if DEBUG:
            HOST = "localhost"
            USER = "test"
            PASSWORD = "password"
            DB = "testdb"
        else:
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


    def create_tfs_collection(self):
        collection = self.mongodb.tfs_matrix
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT PMID, AbstractText FROM MEDLINE_0;")
            rows = cur.fetchall()
            for i, row in enumerate(rows):
                if row[1] is not None & collection.find_one({"pmid": row[0]}) is None:
                    tfs_entry = self.fe.vectorize_corpus([row[1]])
                    post = {
                        "pmid": row[0],
                        "tfs_vector": tfs_entry
                    }
                    collection.insert_one(post).inserted_id

    @staticmethod
    def save_tfs_progress(tfs, pmids):
        # Load tfs storage if available
        tfs_dict = {}
        try:
            tfs_dict = pickle.load(open("tfs_dict.p", "rb"))
        except IOError:
            print 'No tfs_dict was found'
        # Add new entries to dict
        for i, row in enumerate(tfs):
            if pmids[i] not in tfs_dict:
                tfs_dict[pmids[i]] = row
        # Save new map
        pickle.dump(tfs_dict, open("tfs_dict.p", "wb"))

    def load_tfs_progress(self):
        self.tfs_dict = pickle.load(open("tfs_dict.p", "rb"))

    def train_vocabulary(self):
        with self.con:
            cur = self.con.cursor()
            n_articles = "500000"
            cur.execute("SELECT PMID, AbstractText FROM MEDLINE_0 LIMIT" + n_articles + ";")
            for i in range(cur.rowcount):
                row = cur.fetchone()
                if row[1]:
                    self.MapOfAbstracts[row[0]] = row[1]
        extracted_corpus = self.fe.extract_corpus(self.MapOfAbstracts.values())
        tfs = self.fe.vectorize_corpus(extracted_corpus)
        self.save_tfs_progress(tfs, self.MapOfAbstracts.keys())

    def test(self):
        self.load_tfs_progress()
        with self.con:
            con = self.con
            cur = con.cursor()
            n_articles = "500000"
            cur.execute("SELECT PMID, AbstractText FROM MEDLINE_0 LIMIT" + n_articles + ";")
            rows = cur.fetchall()
            for i, row in enumerate(rows):
                if row[1]:
                    if row[0] not in self.tfs_dict:
                        self.MapOfAbstracts[row[0]] = row[1]
        extracted_corpus = self.fe.extract_corpus(self.MapOfAbstracts.values())
        tfs = self.fe.vectorize_corpus(extracted_corpus)
        self.save_tfs_progress(tfs, self.MapOfAbstracts.keys())