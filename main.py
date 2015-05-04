__author__ = 'nathan'

from Medline import Medline

m = Medline()
m.connect_mysql()
m.train_vocabulary(250000)
m.process_abstracts()
m.con.close()

