from fastapi import FastAPI
from pydantic import BaseModel
from rag import generate_response
from rag_qassim import generate_response as generate_response_qassim
from rag_tawhida import generate_response as generate_response_tawhida
from rag_aziza import generate_response as generate_response_aziza

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI with CORS enabled!"}
class LetterRequest(BaseModel):
    letter: str

@app.post("/ask_hannibal/")
async def ask_hannibal(request: LetterRequest):
    print(request.letter)
    ai_reply = generate_response(request.letter)
    return {"response": ai_reply}

@app.post("/ask_qassim/")
async def ask_hannibal(request: LetterRequest):
    print(request.letter)
    ai_reply = generate_response_qassim(request.letter)
    return {"response": ai_reply}


@app.post("/ask_qassim/")
async def ask_hannibal(request: LetterRequest):
    print(request.letter)
    ai_reply = generate_response_tawhida(request.letter)
    return {"response": ai_reply}


@app.post("/ask_aziza/")
async def ask_hannibal(request: LetterRequest):
    print(request.letter)
    ai_reply = generate_response_aziza(request.letter)
    return {"response": ai_reply}