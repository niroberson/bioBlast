__author__ = 'nathan'
import MySQLdb as db

class Medline(object):
    def __init__(self):
        self.MapOfAbstracts = dict()
        self.con = None
        self.pmids = None

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
                    f1.write("%s\n" % pmid)
                    f2.write("%s\n" % abstract)



