import numpy as np
import pandas as pd
import gensim.downloader as api
from gensim.models.doc2vec import TaggedDocument
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

# 学習済みword2vecモデルをロード
w2v_model = api.load('word2vec-google-news-300')

# Define SIF parameters
alpha = 1e-3
freq = 1e-5

# Load network config files
config_files = [
    "config1.txt",
    "config2.txt",
    "config3.txt",
    # add more files as needed
]

# Tokenize and preprocess each config file
tagged_docs = []
for i, file in enumerate(config_files):
    with open(file, 'r') as f:
        content = f.read()
    tokens = content.split()  # replace with your own tokenizer
    preprocessed_tokens = [token.lower() for token in tokens if token.isalpha()] # replace with your own preprocessing steps
    tagged_docs.append(TaggedDocument(preprocessed_tokens, [i]))

# Calculate word weights using SIF formula
word_weights = {}
total_words = sum(w2v_model.vocabulary.values())
for word, freq in w2v_model.vocabulary.items():
    weight = alpha / (alpha + (freq / total_words))
    word_weights[word] = weight

# Calculate document embeddings using SIF formula
doc_embeddings = []
for doc in tagged_docs:
    doc_vector = np.zeros_like(w2v_model['word'])
    word_count = 0
    for word in doc.words:
        if word in w2v_model:
            word_weight = word_weights[word]
            doc_vector += (word_weight * w2v_model[word])
            word_count += 1
    if word_count > 0:
        doc_vector /= word_count
    doc_embeddings.append(doc_vector)

# Cluster documents using KMeans
num_clusters = 5  # replace with your own desired number of clusters
kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(doc_embeddings)

# Calculate cosine similarity matrix between documents
similarity_matrix = cosine_similarity(doc_embeddings)

# Example usage: find documents similar to the first document
query_doc_index = 0
similar_docs_indices = similarity_matrix[query_doc_index].argsort()[::-1][1:6] # replace with your own desired number of similar docs
similar_docs = [config_files[i] for i in similar_docs_indices]
print(f"Documents similar to {config_files[query_doc_index]}: {similar_docs}")

# Example usage: label each document with its corresponding cluster
cluster_labels = kmeans.predict(doc_embeddings)
df = pd.DataFrame({"config_files": config_files, "cluster_labels": cluster_labels})
print(df)
