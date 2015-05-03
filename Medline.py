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
        else:  # Deployed on server
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

    # Finish method if decide to use mongodb
    # def insert_tfs_mongo(self):
    #     collection = self.mongodb.tfs_matrix
    #     cur = self.con.cursor()
    #     cur.execute("SELECT PMID, AbstractText FROM MEDLINE_0 LIMIT 20000;")
    #     rows = cur.fetchall()
    #     for i, row in enumerate(rows):
    #         if row[1] is not None & collection.find_one({"pmid": row[0]}) is None:
    #             tfs_entry = self.fe.vectorize_corpus([row[1]])
    #             post = {
    #                 "pmid": row[0],
    #                 "tfs_vector": tfs_entry
    #             }
    #             collection.insert_one(post).inserted_id

    def process_abstracts(self):
        self.get_tfs_vectors()

    # Create a tfs vector for each abstract, enter into table
    def get_tfs_vectors(self):
        cur = self.con.cursor()
        cur.execute("SELECT PMID, AbstractText FROM MEDLINE_0;")
        cur2 = self.con.cursor()
        for i in range(cur.rowcount):
            row = cur.fetchone()
            if row[1] is not None:
                tfs_vector = pickle.dumps(self.fe.test([row[1]]))
                self.insert_tfs_vector(row[0], tfs_vector)
            if i % 10000 == 0:
                print "Processed" + i + " records"

    # Insert data if it is not in the table
    def insert_tfs_vector(self, pmid, tfs_vector, overwrite=False):
        cur = self.con.cursor()
        record_check = "SELECT (1) FROM bioBlast WHERE pmid = " + pmid + " LIMIT 1;"
        if overwrite is False & cur.execute(record_check) is True:
            return
        # Add mysql query to update if true
        add_record = '''INSERT INTO bioBlast (pmid, tfs_vector) VALUES (%s, %s)'''
        cur.execute(add_record, (pmid, tfs_vector))

    # Train the vocabulary with n entries
    # Needs to be verified that n entries have abstracts
    def train_vocabulary(self):
        with self.con:
            cur = self.con.cursor()
            n_articles = "250000"
            cur.execute("SELECT PMID, AbstractText FROM MEDLINE_0 LIMIT " + n_articles + ";")
            for i in range(cur.rowcount):
                row = cur.fetchone()
                if row[1]:
                    self.mapOfAbstracts[row[0]] = row[1]
        extracted_corpus = self.fe.extract_corpus(self.mapOfAbstracts.values())
        self.fe.train(extracted_corpus)

    # Go through bioBlast table and collect all tfs vectors
    def create_tfs_matrix(self):
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT PMID, tfs_vector FROM bioBlast")
            rows = cur.fetchall()


