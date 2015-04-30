__author__ = 'nathan'


from Medline import Medline

m = Medline()
m.connect_mysql()
# m.train_vocabulary()
m.insert_tfs_mysql()

