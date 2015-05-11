__author__ = 'nathan'
import MySQLdb as db
import pickle
from FeatureExtractor import FeatureExtractor
from pymongo import MongoClient
from scipy.sparse import hstack
import multiprocessing
from contextlib import closing

class Medline(object):
    def __init__(self):
        self.mysql = None
        self.pmids = None
        self.fe = FeatureExtractor()
        self.tfs_dict = None
        self.mongodb = None
        self.mongo_coll = None

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
        self.mysql = db.connect(host=HOST, user=USER, passwd=PASSWORD, db=DB)
        return self.mysql

    def connect_mongo(self, DEBUG=False):
        client = MongoClient()
        if DEBUG:
            test = client.test
            self.mongodb = client.etblast
            self.mongo_coll = client.etblast.test
        else:
            self.mongodb = client.etblast
            self.mongo_coll = client.etblast.bioBlast

    # Finish method if decide to use mongodb
    def insert_tfs_mongo(self, pmid, abstract):
        if self.mongo_coll.find_one({"pmid": pmid}) is None:
            post = {}
            post["pmid"] = pmid
            tfs_vector = pickle.dumps(self.fe.test([abstract]))
            post["tfs_vector"] = tfs_vector
            self.mongo_coll.save(post)

    def queue_process(self, count):
        # Load in the progress of method, call method with correct inputs
        n = 10000
        jobs = []
        for j in range(1, count, n*10):
            for i in range(10):
                mysql = self.connect_mysql()
                x = (i * n) + j
                p = multiprocessing.Process(target=self.process_abstracts, args=(mysql, x, n))
                jobs.append(p)
                p.start()

            for j in jobs:
                j.join()
                
        if count % n * 10 > 0:
            mysql = self.connect_mysql()
            self.process_abstracts(mysql, count - (count % n * 10), count % n * 10)

    # Create a tfs vector for each abstract, enter into table
    def process_abstracts(self, mysql, start=0, limit=0):
        print "Starting: " + str(start) + " to " + str(start + limit)
        with closing( mysql.cursor() ) as cursor:
            cur = self.mysql.cursor()
            mysql_qry = "SELECT PMID, AbstractText FROM MEDLINE_0"
            if start > 0 or limit > 0:
                mysql_qry = mysql_qry + ' LIMIT ' + str(start) + "," + str(limit) + ";"
            else:
                mysql_qry += ";"
            cur.execute(mysql_qry)
            count = 0
            for i in range(cur.rowcount):
                row = cur.fetchone()
                if row[1] is not None:
                    self.insert_tfs_mongo(row[0], row[1])
                    count += 1
        mysql.close()
        print "Exiting: " + str(start) + " to " + str(start + limit) + " with " + str(count) + " abstracts processed."

    # Train the vocabulary with n entries
    # Needs to be verified that n entries have abstracts
    def train_vocabulary(self, n_articles):
        abstract_dict = dict()
        with self.mysql:
            cur = self.mysql.cursor()
            cur.execute("SELECT PMID, AbstractText FROM MEDLINE_0 LIMIT " + str(n_articles) + ";")
            for i in range(cur.rowcount):
                row = cur.fetchone()
                if row[1]:
                    abstract_dict[row[0]] = row[1]
            cur.close()
            self.fe.train(abstract_dict.values())

    # Go through bioBlast table and collect all tfs vectors
    def create_tfs_matrix(self):
        cursor = self.mongo_coll.find()
        pmid_list = []
        tfs_map = {}
        for record in cursor:
            tfs_vector = pickle.loads(record["tfs_vector"])
            tfs_map[record["pmid"]] = tfs_vector
            pmid_list.append(record["pmid"])
        return pmid_list, tfs_map


    def exhaustive_tfs_search(self):
        # Method stub that will search remaining pmids in mysql database that have abstracts but are not in mongodb
        # Then will add the entry to mongodb
        return