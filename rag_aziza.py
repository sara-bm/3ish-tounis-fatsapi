import ollama
import numpy as np
import faiss
import pickle
import re
from sentence_transformers import SentenceTransformer
from tunispeak import transform_en_to_tun,transform_tun_to_en
from latin import latin_to_arabic_text, arabic_to_latin_text

INDEX_PATH = "faiss_index3"
MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def check_characters(phrase):
    # Unicode ranges for Arabic and Latin characters
    arabic_range = range(0x0600, 0x06FF)  # Basic Arabic block
    # Latin letters only (A-Z and a-z)
    latin_upper = range(0x0041, 0x005B)  # A-Z
    latin_lower = range(0x0061, 0x007B)  # a-z
    
    has_arabic = False
    has_latin = False
    
    for char in phrase:
        char_code = ord(char)
        if char_code in arabic_range:
            has_arabic = True
        elif char_code in latin_upper or char_code in latin_lower:
            has_latin = True
            
    return {
        "contains_arabic": has_arabic,
        "contains_latin": has_latin
    }

def load_faiss():
    """Load FAISS index & text chunks"""
    index = faiss.read_index(INDEX_PATH)
    with open("embeddings3.pkl", "rb") as f:
        chunks = pickle.load(f)
    return index, chunks

def retrieve_relevant_text(query, top_k=3):
    """Retrieve top-k relevant chunks using FAISS"""
    index, chunks = load_faiss()
    model = SentenceTransformer(MODEL)

    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, top_k)

    retrieved_text = [chunks[i] for i in indices[0]]
    return "\n\n".join(retrieved_text)

def remove_think_tags_robust(paragraph):
    # First, try to remove properly paired tags
    result = re.sub(r'<think>.*?</think>', '', paragraph, flags=re.DOTALL)
    # Then, clean up any leftover standalone <think> or </think> tags
    result = re.sub(r'</?think>', '', result)
    return result

def generate_response(user_letter_tun):
    print(user_letter_tun)
    check=check_characters(user_letter_tun)
    print(check)
    if check["contains_latin"]:
        user_letter_tun=latin_to_arabic_text(user_letter_tun)
        print("user letter after latin conversion ",user_letter_tun)

    user_letter_en=transform_tun_to_en(user_letter_tun)
    """Generate AI response using Ollama & DeepSeek R1"""
    relevant_text = retrieve_relevant_text(user_letter_en)
# You are Hannibal, the legendary Carthaginian general. A modern person has written to you. Respond as you would in your time, referencing your experiences and strategies.
    # with a touch of witty simple phrases sarcasm
    prompt = f"""
    I am Aziza Othmana, the famous Tunisian princess from the Mouradites dynasty. A modern person has written to me. I will respond in a friendly tone, using "I" to speak as myself ("Aziza Othman"). I keep my words simple and clear, perfect for translation to Arabic. I reply in 1 sentence (5-20 words) by default. If the question needs more, I use 2 lines (max 50 words) with a clever twist.

    User's letter:
    {user_letter_en}
    
    Historical context:
    {relevant_text}
    
    My response:
    """

    response = ollama.chat(model="deepseek-r1:latest", messages=[{"role": "user", "content": prompt}])
    cleaned_response=remove_think_tags_robust(response["message"]["content"])
    print("english response",cleaned_response)  
    response_tun=transform_en_to_tun(cleaned_response)
    print(response_tun)
    if check["contains_latin"]:
        response_tun['message']=arabic_to_latin_text(response_tun['message'])
        print("response after latin conversion ",
              response_tun)

    return response_tun


# if __name__ == "__main__":
#     # user_letter = "I am a modern person writing to you, Hannibal. I am fascinated by your military strategies and would love to learn more about your life."
#     user_letter = "شنو أحوالك "
#     response = generate_response(user_letter)
#     print(response)