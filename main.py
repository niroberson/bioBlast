__author__ = 'nathan'

from Medline import Medline

m = Medline()
m.connect_mysql()
m.train_vocabulary(1000000)
m.connect_mongo()
m.queue_process(0, 24000000)
tfs_matrix, pmid_array = m.create_tfs_map()
similarity = m.tfs_matrix_similarity(tfs_matrix)
m.output_similarity(similarity, pmid_array)