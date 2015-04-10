__author__ = 'nathan'

from Bio import Entrez
Entrez.email = "nathir2@vbi.vt.edu"

handle = Entrez.einfo(db="pubmed")
record = Entrez.read(handle)
handle.close()
print record["DbInfo"]["Count"]


handle = Entrez.esearch(db="pubmed", term="all")
record = Entrez.read(handle)
handle.close()
print record["Count"]
