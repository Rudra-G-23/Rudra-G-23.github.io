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
    
    except Exception as e:
        print("ERROR:", str(e))
I want to create a chat boat for my profile whereas it can answer the user question about my profile and the resume how to build that
Ok I understood upto create a clean text file format folder then used hugging face sentence to transforms then where to store and why to to does I can store in the hugging face but which format need to store extension of the file. 


How to add and is their any effect on asked about this project buttons

How to  show in links of projects. In the chats 


My plan is this create db in the json format and in the hugging face repo. Hugging face gives basic cpu used their I run the   
  
then from user querys goes from fronted which is in the GitHub pages to the fast API then semantic search then LLM then query to the user 
How to create the data.txt file what to write in their and which format tell me does i write the separte txt file format for all does i used md format of writting tell me everthing  
Show me how to auto-convert these files to embeddings
How to create the data.txt file what to write in their and which format tell me does i write the separte txt file format for all does i used md format of writting tell me everthing  

for now give me only the project section 

Open Source
show-file-tree
A small, fast CLI tool to display styled file/folder trees with rich options, colors, icons, and metadata.

PyPI
Docs
GitHub
find-my-joint
A utility to find potential join keys (matching columns) across multiple pandas DataFrames.

PyPI
Docs
GitHub
Featured Projects

Vehicle Insurance Risk Prediction
Insurance companies need to estimate vehicle risk to reduce loss and price policies correctly.

Python • Flask • AWS • Docker

View Project →

• Built end-to-end MLOps pipeline
• Integrated MongoDB + AWS
• CI/CD with GitHub Actions & Docker
• Flask app for real-time prediction

SQL Modern Data Warehouse
ERP & CRM data was inconsistent and not ready for analytics and reporting.

PostgreSQL • SQL • ETL • Star Schema • Power BI

View Project →

• Built Medallion architecture (Bronze–Silver–Gold) for data transformation.
• Developed ETL pipelines integrating ERP & CRM systems.
• Created analytical reports for sales and customer insights.

Yelp Big Data Analysis
Handling large Yelp JSON datasets efficiently without memory issues.

Python • Polars • JSON • Parquet

View Project →


Breast Cancer Prediction App
Need for real-time tumor classification using medical diagnostic features.

Python • Scikit-learn • Streamlit

View Project →


Transportation & Logistic Dashboard
Analyze logistics efficiency to reduce delays and operational costs.

Power BI • KPI Development

View Project →


Smart Transaction Ledger
Smart Transaction Ledger is an AI-powered financial transaction cleaner and fraud detector.

Python • FastAPI • AI • SQL


chatbot-data/projects.txt → your raw knowledge (you already made this)
create_embeddings.py → converts all .txt → data.json
data.json → your searchable memory (text + embedding)
FastAPI app → loads data.json once on startup
/chat endpoint → does semantic search on that memory
then a script for testing the end point

I used groq api key which is present int he .env folder

I have one questions what is the benefits of the [PROJECTS] at top of each project alredy the projects folder it present and it have all the proejcets then why to used this can you tell me 
now giv em eht codde base ont his mental model chatbot-data/projects.txt → your raw knowledge (you already made this)
create_embeddings.py → converts all .txt → data.json
data.json → your searchable memory (text + embedding)
FastAPI app → loads data.json once on startup
/chat endpoint → does semantic search on that memory
then a script for testing the end point

I used groq api key which is present int he .env folder

  File "C:\Users\Rudra\Desktop\Rudra-G-23.github.io\.venv\Lib\site-packages\uvicorn\protocols\http\h11_impl.py", line 415, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Rudra\Desktop\Rudra-G-23.github.io\.venv\Lib\site-packages\uvicorn\middleware\proxy_headers.py", line 56, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Rudra\Desktop\Rudra-G-23.github.io\.venv\Lib\site-packages\fastapi\applications.py", line 1159, in __call__
    await super().__call__(scope, receive, send)
  File "C:\Users\Rudra\Desktop\Rudra-G-23.github.io\.venv\Lib\site-packages\starlette\applications.py", line 90, in __call__
    await self.middleware_stack(scope, receive, send)
  File "C:\Users\Rudra\Desktop\Rudra-G-23.github.io\.venv\Lib\site-packages\starlette\middleware\errors.py", line 186, in __call__
    raise exc
  File "C:\Users\Rudra\Desktop\Rudra-G-23.github.io\.venv\Lib\site-packages\starlette\middleware\errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "C:\Users\Rudra\Desktop\Rudra-G-23.github.io\.venv\Lib\site-packages\starlette\middleware\exceptions.py", line 63, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "C:\Users\Rudra\Desktop\Rudra-G-23.github.io\.venv\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "C:\Users\Rudra\Desktop\Rudra-G-23.github.io\.venv\Lib\site-packages\starlette\_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "C:\Users\Rudra\Desktop\Rudra-G-23.github.io\.venv\Lib\site-packages\fastapi\middleware\asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "C:\Users\Rudra\Desktop\Rudra-G-23.github.io\.venv\Lib\site-packages\starlette\routing.py", line 660, in __call__
    await self.middleware_stack(scope, receive, send)
  File "C:\Users\Rudra\Desktop\Rudra-G-23.github.io\.venv\Lib\site-packages\starlette\routing.py", line 680, in app
    await route.handle(scope, receive, send)
  File "C:\Users\Rudra\Desktop\Rudra-G-23.github.io\.venv\Lib\site-packages\starlette\routing.py", line 276, in handle
    await self.app(scope, receive, send)
  File "C:\Users\Rudra\Desktop\Rudra-G-23.github.io\.venv\Lib\site-packages\fastapi\routing.py", line 134, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "C:\Users\Rudra\Desktop\Rudra-G-23.github.io\.venv\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "C:\Users\Rudra\Desktop\Rudra-G-23.github.io\.venv\Lib\site-packages\starlette\_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "C:\Users\Rudra\Desktop\Rudra-G-23.github.io\.venv\Lib\site-packages\fastapi\routing.py", line 120, in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
  File "C:\Users\Rudra\Desktop\Rudra-G-23.github.io\.venv\Lib\site-packages\fastapi\routing.py", line 674, in app
    raw_response = await run_endpoint_function(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Rudra\Desktop\Rudra-G-23.github.io\.venv\Lib\site-packages\fastapi\routing.py", line 330, in run_endpoint_function
    return await run_in_threadpool(dependant.call, **values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Rudra\Desktop\Rudra-G-23.github.io\.venv\Lib\site-packages\starlette\concurrency.py", line 32, in run_in_threadpool
    return await anyio.to_thread.run_sync(func)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Rudra\Desktop\Rudra-G-23.github.io\.venv\Lib\site-packages\anyio\to_thread.py", line 63, in run_sync
    return await get_async_backend().run_sync_in_worker_thread(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Rudra\Desktop\Rudra-G-23.github.io\.venv\Lib\site-packages\anyio\_backends\_asyncio.py", line 2518, in run_sync_in_worker_thread
    return await future
           ^^^^^^^^^^^^
  File "C:\Users\Rudra\Desktop\Rudra-G-23.github.io\.venv\Lib\site-packages\anyio\_backends\_asyncio.py", line 1002, in run
    result = context.run(func, *args)
             ^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Rudra\Desktop\Rudra-G-23.github.io\main.py", line 83, in chat
    response = client.chat.completions.create(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Rudra\Desktop\Rudra-G-23.github.io\.venv\Lib\site-packages\groq\resources\chat\completions.py", line 461, in create
    return self._post(
           ^^^^^^^^^^^
  File "C:\Users\Rudra\Desktop\Rudra-G-23.github.io\.venv\Lib\site-packages\groq\_base_client.py", line 1284, in post
    return cast(ResponseT, self.request(cast_to, opts, stream=stream, stream_cls=stream_cls))
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Rudra\Desktop\Rudra-G-23.github.io\.venv\Lib\site-packages\groq\_base_client.py", line 1071, in request
    raise self._make_status_error_from_response(err.response) from None
groq.BadRequestError: Error code: 400 - {'error': {'message': 'The model llama3-8b-8192 has been decommissioned and is no longer supported. Please refer to https://console.groq.com/docs/deprecations for a recommendation on which model to use instead.', 'type': 'invalid_request_error', 'code': 'model_decommissioned'}}
why this happens Responses
Curl

curl -X 'POST' \
  'https://rudra-g-23-rudra-portfolio-rag-chatbot-api.hf.space/chat' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "question": "what is the full name of the rudra"
}'
Request URL
https://rudra-g-23-rudra-portfolio-rag-chatbot-api.hf.space/chat
Server response
Code	Details
500
Undocumented
Error: response status is 500

Response body
Download
Internal Server Error
Response headers
 access-control-allow-credentials: true 
 access-control-allow-origin: https://rudra-g-23-rudra-portfolio-rag-chatbot-api.hf.space 
 content-length: 21 
 content-type: text/plain; charset=utf-8 
 date: Tue,05 May 2026 15:27:15 GMT 
 link: <https://huggingface.co/spaces/Rudra-G-23/rudra-portfolio-rag-chatbot-api>;rel="canonical" 
 server: uvicorn 
 vary: origin,access-control-request-method,access-control-request-headers 
 x-proxied-host: http://10.111.86.141 
 x-proxied-path: /chat 
 x-proxied-replica: f2dwg7mi-27d52gbzh 
 x-request-id: d3x-U8 import json
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
why this happens 
Code	Details
500
Undocumented
Error: Internal Server Error

Response body
Download
Internal Server Error
Response headers
 content-length: 21 
 content-type: text/plain; charset=utf-8 
 date: Tue,05 May 2026 16:08:52 GMT 
 server: uvicorn import json
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
    query_embedding = get_model.encode(query)

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
    
    except Exception as e:
        print("ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))