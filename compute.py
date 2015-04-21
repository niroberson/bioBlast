__author__ = 'nathan'
# Code to access MEDLINE tables

import MySQLdb as db
from FeatureExtractor import FeatureExtractor


# Setup connection to etblast databse
HOST = 'localhost'
USER = "johnny"
PASSWORD = "johnny"
DB = "etblast"

con = db.connect(host=HOST, user=USER, passwd=PASSWORD, db=DB)


# Create feature extractor object
fe = FeatureExtractor()

compiled_corpus = []

with con:

    cur = con.cursor()
    cur.execute("SELECT AbstractText FROM MEDLINE_0_old limit 200;")

    for i in range(cur.rowcount):

        row = cur.fetchone()
        if row:
            compiled_corpus += row[0]

extracted = fe.extract_corpus(compiled_corpus)
tfs = fe.vectorize_corpus(extracted)
cosine_mat = fe.compute_cosine(tfs)
print cosine_mat