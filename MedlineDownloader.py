__author__ = 'nathan'
# Code to access MEDLINE tables

import MySQLdb as mdb

con = mdb.connect('localhost', 'johnny', 'johnny', 'etblast');

with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM MEDLINE_2014_abstracts")

    for i in range(10):
        row = cur.fetchone()
        print row[0], row[1]