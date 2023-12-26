import sqlite3
import numpy as np
from sklearn.manifold import TSNE
from sklearn.cluster import DBSCAN
import plotly.graph_objects as go
from sklearn.metrics import pairwise_distances

# Connect to the SQLite database
conn = sqlite3.connect('arxiv-ai-ml-papers.db')
cursor = conn.cursor()

# Get the vectorized data from the database
cursor.execute("SELECT id, title, Published, title_embedding, abstract_embedding FROM papers")
rows = cursor.fetchall()

# Unpack the data into separate lists
ids, titles, dates, title_vectors, abstract_vectors = zip(*rows)
title_vectors = [np.frombuffer(row, dtype=np.float32) for row in title_vectors]
abstract_vectors = [np.frombuffer(row, dtype=np.float32) for row in abstract_vectors]

# Concatenate title and abstract vectors
vectors = np.concatenate((title_vectors, abstract_vectors), axis=1)

# Use t-SNE to reduce the dimensionality of the vectors to 3 dimensions

tsne = TSNE(n_components=3, perplexity=10)
reduced_vectors = tsne.fit_transform(vectors)

# Use DBSCAN to identify clusters
clustering = DBSCAN(eps=3, min_samples=2).fit(reduced_vectors)
labels = clustering.labels_

# Compute pairwise distances
distances = pairwise_distances(reduced_vectors)

# For each point, find the smallest non-zero distance
min_distances = np.min(distances + np.eye(distances.shape[0]) * np.max(distances), axis=1)

# Normalize distances to [0, 1] range for coloring
min_distances = (min_distances - min_distances.min()) / (min_distances.max() - min_distances.min())

# Create a 3D scatter plot of the reduced vectors
fig = go.Figure(data=[go.Scatter3d(
    x=reduced_vectors[:, 0],
    y=reduced_vectors[:, 1],
    z=reduced_vectors[:, 2],
    mode='markers',
    marker=dict(
        size=6,
        color=min_distances,    # set color to minimum distances
        colorscale='Bluered',   # choose a colorscale
        opacity=0.5
    ),
    text=[f'Title: {title}<br>Link: https://arxiv.org/abs/{id}<br>Published: {date}' for title, id, date in zip(titles, ids, dates)],
    hoverinfo='text'
)])

fig.update_layout(hovermode='closest')

fig.show()

# Close the database connection
conn.close()