import pinecone
import numpy as np
from sklearn.manifold import TSNE

# Initialize Pinecone
pinecone.init(api_key='90e6e2e9-31f1-4ff2-9629-0f4bcf990a8e', environment='us-west4-gcp-free') 
index = pinecone.Index('chart3d') 

def fetch_vectors():
    # Read the vector ids from the file
    with open('ids.txt', 'r') as f:
        vector_ids = [line.strip() for line in f]

    # Fetch the vectors
    vectors = index.fetch(ids=vector_ids)

    # Convert the vectors to a 2D numpy array
    X = np.array([vectors[id] for id in vector_ids])

    return X

def reduce_dimensionality(X):
    # Perform t-SNE
    X_embedded = TSNE(n_components=3).fit_transform(X)

    return X_embedded

def main():
    # Fetch the vectors
    X = fetch_vectors()

    # Reduce dimensionality
    X_embedded = reduce_dimensionality(X)

    print(X_embedded)

if __name__ == "__main__":
    main()
