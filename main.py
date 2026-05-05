import json
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from groq import Groq
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Rudra Portfolio Chatbot API")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

CHATBOT_DATA_URL = r"https://raw.githubusercontent.com/Rudra-G-23/Rudra-G-23.github.io/refs/heads/main/chatbot-data/data.json"
response = requests.get(CHATBOT_DATA_URL)
DATA = response.json()

# Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class Query(BaseModel):
    question: str


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def search(query, top_k=3):
    query_embedding = model.encode(query)

    scores = []
    for item in DATA:
        score = cosine_similarity(query_embedding, np.array(item["embedding"]))
        scores.append((score, item))

    scores.sort(reverse=True)

    return [item["text"] for score, item in scores[:top_k]]


@app.post("/chat")
def chat(query: Query):
    context_chunks = search(query.question)
    context = "\n\n".join(context_chunks)

    prompt = f"""
You are a professional AI assistant representing Rudra Prasad Bhuyan.

Your job is to answer questions ONLY based on the provided context.

Rules:
- Do not add any information outside the context
- If answer is not found, say: "I don't have that information"
- Keep answers clear and structured
- Always highlight project names
- Always include project links if available

Formatting rules:
- Use bullet points for multiple items
- For each project:
  - Name
  - Short description (1–2 lines)
  - Key technologies
  - Project link

Tone:
- Professional
- Clear
- Concise

Context:
{context}

Question:
{query.question}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "answer": response.choices[0].message.content
    }