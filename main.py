__author__ = 'nathan'


from Medline import Medline

m = Medline()
m.connect_mysql()
m.train_vocabulary()
m.tfs_insert_mysql_linear()

