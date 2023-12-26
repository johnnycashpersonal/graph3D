### DO NOT EDIT THIS AGAIN ###

import sqlite3

conn = sqlite3.connect('arxiv-ai-ml-papers.db')

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE papers(
        id TEXT PRIMARY KEY,
        title TEXT,
        abstract TEXT,
        title_embedding BLOB,
        abstract_embedding BLOB)
''')
conn.commit()
conn.close()

