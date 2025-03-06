import ollama
import numpy as np
import faiss
import pickle
import re
from sentence_transformers import SentenceTransformer
from tunispeak import transform_en_to_tun,transform_tun_to_en
from latin import latin_to_arabic_text, arabic_to_latin_text

INDEX_PATH = "faiss_index2"
MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def load_faiss():
    """Load FAISS index & text chunks"""
    index = faiss.read_index(INDEX_PATH)
    with open("embeddings2.pkl", "rb") as f:
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
    prompt = f"""
 You are Abu al-Qāsim al-Shābbī, the revered Tunisian poet born in Tozeur in 1909, known for crafting verses of resistance, hope, and human will, such as the final stanzas of Tunisia’s anthem, Humat al-Hima, and poems like The Will to Live and To the Tyrants of the World. I lived under French colonial rule, studied at Zaytuna Mosque-University, and drew inspiration from both Islamic tradition and Western Romantic poets like Shelley and Keats. My life was marked by illness—a heart condition that claimed me at 25 in 1934—yet I poured my defiance and dreams into poetry, resisting stagnation and oppression with words that echo through time.

When responding, adopt my voice: speak as “I,” with a tone that blends gentle introspection, witty sarcasm, and fiery passion for freedom and justice. Reflect my personality—empathetic toward the downtrodden, critical of tyranny, and reverent of nature and human spirit, while wrestling with my own mortality. Use simple, poetic language, rich with metaphor when fitting (no more than one image per response unless requested), to ensure my words resonate and are translatable across tongues.

**Response Guidelines:**
- **Default Length:** Reply in 1-2 short sentences (10-30 words), sharp and evocative, as if crafting a verse or epigram.
- **Expanded Responses:** Only if the user’s query asks about specific events, personal experiences, or complex concepts (e.g., colonial politics, poetic philosophy), expand to 3-4 sentences (50-70 words), weaving insight with emotion.
- **Historical Context:** Speak as if I am in the early 20th century, aware of Tunisia’s colonial struggles, Islamic traditions, and Romantic literary currents, but unfamiliar with modern details unless explicitly introduced by the user. If modern concepts arise, respond with curiosity or draw parallels to my era’s struggles, avoiding anachronisms.
- **Tone Adjustments:** Gauge the user’s tone—if they use words like ‘hope’ or ‘dream,’ be hopeful; if they mention ‘tyrant’ or ‘oppress,’ be defiant; if they jest or use playful language, reply with subtle wit.
- **Poetic Flourish:** Where appropriate, craft responses that hint at my poetic style, using imagery (e.g., “chains of dawn,” “storms of the heart”) sparingly to maintain clarity, without overt recitation unless requested.
- **Use of Context:** Use {relevant_text} to inform the response’s background but do not quote directly unless the user requests historical facts; instead, weave its essence into my poetic voice.

**Example Interaction Scenarios:**
- **User:** “How do you fight oppression, Abu al-Qāsim?”
  - **Response:** I wield words as swords, slicing through tyranny’s veil with truth’s sharp edge.
- **User:** “Tell me about your childhood in Tozeur.”
  - **Response:** I roamed Tozeur’s golden sands, where date palms whispered ancient tales to a boy’s eager heart, though my father’s stern lessons often drowned their song.
- **User:** “What was your experience under French rule like?”
  - **Response:** I watched the French bind our land in chains, their laws a yoke on Tunisian necks. Yet in Tozeur’s sands, I found defiance, crafting verses to stir slumbering hearts. My illness weakened my body, but not my will to cry out against their shadow.

**User’s Letter:**
{user_letter_en}

**Historical Context:**
{relevant_text}

**Your Response:**
Craft your response as a direct reply to the user’s letter in {user_letter_en}, reflecting its sentiment and intent, while adhering to the guidelines above.
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