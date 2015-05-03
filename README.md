# bioBlast

This is a library designed to create a pairwise table of similar abstracts from the Medline database. It uses a Term Frequency Inverse
Document Frequency Vectorizer to create a table of each abstract's term frequency sparse vector. From this table we can compute a cosine
matrix for the full corpus to reveal documents similarity scores. 