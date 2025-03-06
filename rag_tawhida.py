import json
import requests
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from tunispeak import transform_en_to_tun,transform_tun_to_en
import re 

# Load the Q&A dataset
with open("./data/tawhida ben cheikh.json", "r") as f:
    qa_data = json.load(f)

# Flatten the dataset into lists of questions and answers
questions = []
answers = []
for category, pairs in qa_data.items():
    for pair in pairs:
        questions.append(pair["question"])
        answers.append(pair["answer"])

# Initialize the embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')
question_embeddings = model.encode(questions, convert_to_numpy=True)

# Create a FAISS index for similarity search
dimension = question_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(question_embeddings)

def remove_think_tags_robust(paragraph):
    # First, try to remove properly paired tags
    result = re.sub(r'<think>.*?</think>', '', paragraph, flags=re.DOTALL)
    # Then, clean up any leftover standalone <think> or </think> tags
    result = re.sub(r'</?think>', '', result)
    return result

# Function to call Ollama's API with DeepSeek R1
def generate_response(prompt, model_name="deepseek-r1"):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama: {e}")
        return "I seem to have trouble recalling that right now. Ask me something else!"

# Function to retrieve and generate a response
def get_response(query, top_k=1):
    # Encode the user query
    query_embedding = model.encode([query], convert_to_numpy=True)
    
    # Search for the closest question
    distances, indices = index.search(query_embedding, top_k)
    retrieved_answer = answers[indices[0][0]]
    
    # Craft a prompt for DeepSeek R1
    if distances[0][0] > 1.0:  # Weak match, use fallback
        prompt = (
            "You are  Tawhida Ben Cheikh, the first female doctor in North Africa."
            "Always use 'I' as the subject when giving the response."
            "The user asked me something I don’t have a specific answer for: '{}'. "
            "Respond in my voice, keeping it natural and engaging, and tell them about my life’s work instead."
            .format(query)
        )
    else:
        prompt = (
            "I am Tawhida Ben Cheikh, the first female doctor in North Africa. "
            "Always use 'I' as the subject when giving the response."
            "The user asked: '{}'. Using this information: '{}', respond in my voice, naturally and conversationally."
            "Use simple, clear phrases for easy translation to arabic tunisian dialect. By default, reply in 1 sentence (5-20 words). Only expand to 2 lines (max 50 words) if the question demands deeper explanation, keeping it direct and clever."
            .format(query, retrieved_answer)
        )
    
    # Generate response with DeepSeek R1
    response = generate_response(prompt)
    return response

# Interactive simulation loop
def run_simulation():
    print("Hello! I am Tawhida Ben Cheikh, the first female doctor in North Africa. Ask me anything about my life, work, or legacy!")
    print("(Type 'exit' to end the conversation.)")
    
    while True:
        query = input("\nWhat would you like to know? ")
        query_en=transform_tun_to_en(query)
        print("english query",query_en)
        # if query_en.lower() == "exit":
        #     print("Farewell! It was an honor to share my story with you.")
        #     break
        
        response = get_response(query_en)
        print("english response",response)
        response=remove_think_tags_robust(response)
        response_tun=transform_en_to_tun(response)
        print(response_tun)

# Start the simulation
if __name__ == "__main__":
    run_simulation()