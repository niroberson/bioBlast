__author__ = 'nathan'


from Medline import Medline

m = Medline()
m.connect_mysql()
# # m.get_pmids()
# m.get_abstracts()
#m.extract_corpus()
m.train_vocabulary()
m.put_tfs_in_mysql()

