import sqlite3
# Connect to the SQLite database
conn = sqlite3.connect('arxiv-ai-ml-papers.db')
cursor = conn.cursor()

# Add a new column "Published" to the "papers" table
cursor.execute("ALTER TABLE papers ADD COLUMN Published TEXT")

# Commit the changes and close the connection
conn.commit()
conn.close()
