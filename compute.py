__author__ = 'nathan'
# Code to access MEDLINE tables

import MySQLdb as db
from FeatureExtractor import FeatureExtractor


# Setup connection to etblast databse
HOST = 'localhost'
PORT = 3306
USER = "johnny"
PASSWORD = "johnny"
DB = "etblast"

con = db.connect(host=HOST, user=USER, passwd=PASSWORD, db=DB)


# Create feature extractor object
fe = FeatureExtractor()


with con:

    cur = con.cursor()
    cur.execute("SELECT AbstractText FROM MEDLINE_2014_0 LIMIT 1;")

    for i in range(cur.rowcount):

        row = cur.fetchone()
        print row

        stemmed = fe.stem_tokens(row[1])
        print stemmed