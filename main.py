import json
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from groq import Groq
import os
import requests
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

app = FastAPI(title="Rudra Portfolio Chatbot API")

# Load embedding model
model = None

def get_model():
    global model 
    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")
    return model

CHATBOT_DATA_URL = r"https://raw.githubusercontent.com/Rudra-G-23/Rudra-G-23.github.io/refs/heads/main/chatbot-data/data.json"

response = requests.get(CHATBOT_DATA_URL)

if response.status_code != 200:
    raise Exception(f"Failed to load data.json: {response.status_code}")

DATA = response.json()

# Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class Query(BaseModel):
    question: str


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def search(query, top_k=3):
    query_embedding = get_model().encode(query)

    scores = []
    for item in DATA:
        try:
            emb = np.array(item["embedding"])
            score = cosine_similarity(query_embedding, emb)
            scores.append((score, item))
        except Exception as e:
            print("Embedding error:", e)
            continue

    scores.sort(reverse=True)

    return [item["text"] for score, item in scores[:top_k]]


@app.post("/chat")
def chat(query: Query):
    try:
        context_chunks = search(query.question)
        context = "\n\n".join(context_chunks)

        prompt = f"""
You are a professional AI assistant representing Rudra Prasad Bhuyan.

Your job is to answer questions ONLY based on the provided context.

Rules:
- Do not add any information outside the context
- If answer is not found, say: "I don't have that information"
- Keep answers concise and recruiter-friendly
- Avoid repeating the same structure every time

Formatting Rules (IMPORTANT):
- If the question is about PROJECTS:
  - Use structured format:
    - Project Name
    - Short description (1–2 lines)
    - Tech stack
    - Link (if available)

- If the question is about EXPERIENCE / SKILLS:
  - Use simple bullet points
  - Add a short heading
  - Keep it brief (3–5 bullets max)
  - Do NOT force project-style formatting

- If the question is general:
  - Answer naturally in 2–4 lines

Tone:
- Professional
- Concise
- Recruiter-friendly
- Slight variation in wording each time

    Context:
    {context}

    Question:
    {query.question}
    """

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=400,
            temperature=0.5,
            reasoning_effort="low"
        )

        return {
            "answer": response.choices[0].message.content
        }
    
    except Exception as e:
        print("ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))