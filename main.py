__author__ = 'nathan'

from Medline import Medline
import os.path

m = Medline()

# Connect to mysql and train and save vocab
m.connect_mysql()
m.train_vocabulary(250000)

# Connect to mysql, mongo and process all abstracts
m.connect_mysql()
m.connect_mongo()
m.queue_process(2400000)
