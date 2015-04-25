__author__ = 'nathan'
from Bio import Entrez
from Bio import Medline
Entrez.email = "nathir2@vbi.vt.edu"

class Article(object):

    def __init__(self, pmid):
        self.pmid = pmid
        self.pmcid = None
        self.abstract = None
        self.authors = None
        self.journal = None
        self.date = None

    def fill_all_fields(self):
        handle = Entrez.efetch(db="pubmed", id=self.pmid, rettype="medline", retmode="text")
        record = Medline.read(handle)
        if "AB" in record:
            self.abstract = record["AB"]
        if "FAU" in record:
            self.authors = record["FAU"]
        if "TI" in record:
            self.title = record["TI"]
        if "DP" in record:
            self.date = record["DP"]
        if "JT" in record:
            self.journal = record["JT"]
        if "PMCID" in record:
            self.pmcid = record["PMCID"]

    def get_abstract(self):
        handle = Entrez.efetch(db="pubmed", id=self.pmid, rettype="medline", retmode="text")
        record = Medline.read(handle)
        if "AB" in record:
            self.abstract = record["AB"]