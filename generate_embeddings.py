# generate_faiss_index.py
import pandas as pd
from utils.faiss_utils import generate_embeddings, create_faiss_index, save_faiss_index, save_faq_data

# Load the FAQ CSV file
faq_df = pd.read_csv("./data/customer-service-qa.csv")

# Generate embeddings for the FAQ questions
faq_embeddings = generate_embeddings(faq_df)

# Create FAISS index for the embeddings
index = create_faiss_index(faq_embeddings)

# Save the FAISS index and FAQ data
save_faiss_index(index, "./data/faq_index.bin")
# save_faq_data(faq_df, "./data/faq_data.csv")
