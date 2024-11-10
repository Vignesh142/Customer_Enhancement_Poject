# faiss_utils.py
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

def generate_embeddings(faq_df, model_name='all-MiniLM-L6-v2'):
    """Generates embeddings for FAQ questions."""
    model = SentenceTransformer(model_name)
    faq_questions = faq_df['question'].tolist()
    faq_embeddings = model.encode(faq_questions)
    return faq_embeddings

def create_faiss_index(faq_embeddings):
    """Creates a FAISS index for the FAQ embeddings."""
    dimension = faq_embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(faq_embeddings).astype('float32'))
    return index

def save_faiss_index(index, file_path="faq_index.bin"):
    """Saves the FAISS index to a file."""
    faiss.write_index(index, file_path)

def load_faiss_index(file_path="faq_index.bin"):
    """Loads the FAISS index from a file."""
    return faiss.read_index(file_path)

def save_faq_data(faq_df, file_path="faq_data.csv"):
    """Saves the FAQ data to a CSV file."""
    faq_df.to_csv(file_path, index=False)

def load_faq_data(file_path="faq_data.csv"):
    """Loads the FAQ data from a CSV file."""
    return pd.read_csv(file_path)

def search_similar_faq(query, index, faq_df, model, top_k=1):
    """Searches for the most similar FAQ to the customer query using the FAISS index."""
    query_embedding = model.encode([query]).astype('float32')
    distances, indices = index.search(query_embedding, top_k)
    
    if indices[0][0] != -1:
        faq_answer = faq_df.iloc[indices[0][0]]['answer']
        similarity_score = distances[0][0]
        print(similarity_score, faq_answer)
        return faq_answer, similarity_score
    else:
        return None, None
