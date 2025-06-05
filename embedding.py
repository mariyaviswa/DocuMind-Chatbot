from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


#----------------------------------
# Model 
#----------------------------------
model = SentenceTransformer('all-MiniLM-L6-v2') 

def chunk_text(text, chunk_size=500, overlap=100):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

#------------------------------
# Split into Chunks
#------------------------------
def embed_chunks(chunks):
    return model.encode(chunks, convert_to_numpy=True)

def build_faiss_index(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index

def embed_document(text):
    chunks = chunk_text(text)
    embeddings = embed_chunks(chunks)
    index = build_faiss_index(embeddings)
    return index, chunks, embeddings

#--------------------------------------------
# Match top k chunks 
#--------------------------------------------
def search_similar_chunks(query, model, faiss_index, chunks, top_k=3):
    query_embedding = model.encode([query])[0]
    D, I = faiss_index.search(np.array([query_embedding]), top_k)
    results = [chunks[i] for i in I[0]]
    return results
