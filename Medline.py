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
            cur.execute("SELECT PMID, AbstractText FROM MEDLINE_0 LIMIT 200;")
            pmids=[]
            abstracts=[]
            for i in range(cur.rowcount):
                row = cur.fetchone()
                if row[0] & row[1]:
                    pmids.append(row[0])
                    abstracts.append(row[1])
            f = open('abstracts.txt', 'w')
            for index, abstract in abstracts:
                f.write("%s\n" % abstract)

            f = open('pmids2.txt', 'w')
            for pmid in pmids:
                f.write("%s\n" % pmid)





