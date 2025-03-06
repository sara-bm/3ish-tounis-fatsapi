import fitz  # PyMuPDF
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

PDF_PATH = "./data/hannibal.pdf"
PDF_PATH2 = "./data/Abou Qassim Bio.pdf"
PDF_PATH3 = "./data/Aziza Othmana.pdf"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # Small & efficient

def extract_text(pdf_path):
    """Extract text from a PDF file"""
    doc = fitz.open(pdf_path)
    text_chunks = [page.get_text("text") for page in doc]
    return text_chunks

def embed_text(chunks, model):
    """Generate embeddings for text chunks"""
    embeddings = model.encode(chunks, convert_to_numpy=True, show_progress_bar=True)
    return embeddings

def save_faiss_index(embeddings, chunks,embeddings_name, index_path):
    """Save embeddings to FAISS"""
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    with open(embeddings_name, "wb") as f:
        pickle.dump(chunks, f)

    faiss.write_index(index, index_path)

def load_faiss_index(embeddings_name,index_path):
    """Load FAISS index"""
    index = faiss.read_index(index_path)
    with open(embeddings_name, "rb") as f:
        chunks = pickle.load(f)
    return index, chunks

if __name__ == "__main__":
    print("Extracting text from PDF...")
    text_chunks = extract_text(PDF_PATH)
    text_chunks2 = extract_text(PDF_PATH2)
    text_chunks3 = extract_text(PDF_PATH3)
    print("Generating embeddings...")
    model = SentenceTransformer(EMBEDDING_MODEL)
    embeddings = embed_text(text_chunks, model)
    embeddings2 = embed_text(text_chunks2, model)
    embeddings3 = embed_text(text_chunks3, model)
    print("Saving embeddings to FAISS...")
    save_faiss_index(embeddings,text_chunks, "embeddings.pkl", "faiss_index")
    save_faiss_index(embeddings2, text_chunks2, "embeddings2.pkl", "faiss_index2")
    save_faiss_index(embeddings3, text_chunks3, "embeddings3.pkl", "faiss_index3")
    print("Embedding process complete!")

