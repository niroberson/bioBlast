__author__ = 'nathan'
# Code to access MEDLINE tables

import MySQLdb as mdb
from FeatureExtractor import FeatureExtractor


# Setup connection to etblast databse
con = mdb.connect('localhost', 'johnny', 'johnny', 'etblast')

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