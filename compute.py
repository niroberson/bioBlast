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


with con:

    cur = con.cursor()
    cur.execute("SELECT AbstractText FROM MEDLINE_0_old limit 200;")

    for i in range(cur.rowcount):

        row = cur.fetchone()
        row = row[0]
        if row:
            extracted = fe.extract_entry(row)
            fe.initialize_vectorize()
            fe.fit_transform_entry(extracted)

    cosine_mat = fe.compute_cosine(fe.tfs)
    print cosine_mat