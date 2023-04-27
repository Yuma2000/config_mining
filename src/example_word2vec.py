"""
word2vecを使ったシステム．
"""
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import os


def preprocess_text(text):
    """
    Define a function to preprocess the text data
    """
    tokens = word_tokenize(text)
    return tokens


def load_configs(folder_path):
    """
    Define a function to load the configuration files
    """
    configs = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r') as f:
                text = f.read()
                configs.append(text)
    return configs


def train_doc2vec_model(configs):
    """
    Define a function to train the Doc2Vec model
    """
    tagged_data = [TaggedDocument(words=preprocess_text(text), tags=[str(i)]) for i, text in enumerate(configs)]
    model = Doc2Vec(vector_size=100, min_count=1, epochs=20)
    model.build_vocab(tagged_data)
    model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)
    return model


# コンフィグフォルダのpath
configs_folder_path = '/path/to/configs/folder'
configs = load_configs(configs_folder_path)

# Doc2Vec モデルを学習する．
model = train_doc2vec_model(configs)

# Get the embedding for a specific config block
config_block = 'sample config block'
embedding = model.infer_vector(preprocess_text(config_block))

# Use the embedding to find similar config blocks
similar_blocks = model.docvecs.most_similar([embedding], topn=5)

# 似ているブロックを出力する．
for block in similar_blocks:
    print(configs[int(block[0])])
