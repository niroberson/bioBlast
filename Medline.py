__author__ = 'nathan'
import MySQLdb as db
import pickle
from FeatureExtractor import FeatureExtractor
import sys

class Medline(object):
    def __init__(self):
        self.MapOfAbstracts = dict()
        self.con = None
        self.pmids = None
        self.fe = FeatureExtractor()

    def connect(self):
        # Setup connection to etblast databse
        HOST = 'localhost'
        USER = "johnny"
        PASSWORD = "johnny"
        DB = "etblast"

        self.con = db.connect(host=HOST, user=USER, passwd=PASSWORD, db=DB)

    def get_pmids(self):
        with self.con:
            con = self.con
            cur = con.cursor()
            cur.execute("SELECT PMID FROM MEDLINE_0;")
            pmids = []
            for i in range(cur.rowcount):
                row = cur.fetchone()
                if row:
                    pmids.append(row)

            self.pmids = pmids
            f = open('pmids.txt', 'w')
            for pmid in pmids:
                f.write("%s\n" % pmid)

            f.close()

    def get_abstracts(self):
        with self.con:
            con = self.con
            cur = con.cursor()
            cur.execute("SELECT PMID, AbstractText FROM MEDLINE_0;")

            f1 = open('pmids2.txt', 'w')
            f2 = open('abstracts.txt', 'w')
            for i in range(cur.rowcount):
                row = cur.fetchone()
                if row[1]:
                    f1.write("%s\n" % row[0])
                    f2.write("%s\n" % row[1])
            f1.close()
            f2.close()

    def extract_corpus(self):
        with self.con:
            con = self.con
            cur = con.cursor()
            cur.execute("SELECT PMID, AbstractText FROM MEDLINE_0;")
            for i in range(cur.rowcount):
                row = cur.fetchone()
                if row[1]:
                    self.MapOfAbstracts[row[0]] = row[1]
            pickle.dump(self.MapOfAbstracts, open("MapOfAbstracts.p", "wb"))

    def compute(self):
        self.MapOfAbstracts = pickle.load(open("MapOfAbstracts.p", "rb"))
        extracted_corpus = self.fe.extract_corpus(self.MapOfAbstracts.values())
        tfs = self.fe.vectorize_corpus(extracted_corpus)
        cosine_matrix = self.fe.compute_cosine(tfs)

    def train(self):
        with self.con:
            con = self.con
            cur = con.cursor()
            cur.execute("SELECT PMID, AbstractText FROM MEDLINE_0 LIMIT 200000;")
            for i in range(cur.rowcount):
                row = cur.fetchone()
                if row[1]:
                    self.MapOfAbstracts[row[0]] = row[1]
        extracted_corpus = self.fe.extract_corpus(self.MapOfAbstracts.values())
        self.fe.vectorize_corpus(extracted_corpus)

    def test(self):
        with self.con:
            con = self.con
            cur = con.cursor()
            n_articles = "500000"
            cur.execute("SELECT PMID, AbstractText FROM MEDLINE_0 LIMIT" + n_articles + ";")
            rows = cur.fetchall()
            for i, row in enumerate(rows):
                if i % 100000 == 0:
                    self.update_progress(i)
                if row[1]:
                    self.MapOfAbstracts[row[0]] = row[1]
        extracted_corpus = self.fe.extract_corpus(self.MapOfAbstracts.values())
        tfs = self.fe.vectorize_corpus(extracted_corpus)
        pickle.dump(tfs, open("tfs_sparse.p", "wb"))
        # tfs_dict = dict()
        # pmids = self.MapOfAbstracts.keys()
        # # for i, row in enumerate(tfs):
        # #     tfs_dict[pmids[i]] = row
        # # cosine_matrix = fe.compute_cosine(tfs)

    @staticmethod
    def update_progress(progress):
        print '\r{0}%'.format(progress)