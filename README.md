# Rudra Prasad Bhuyan Portfolio

Live site: https://rudra-g-23.github.io/

## Run locally

The portfolio is a static website. From the repository root, start a local web server:

```bash
python3 -m http.server 8080
```

Open http://localhost:8080 in your browser. The website's chatbot continues to use the deployed API by default.

## Run the chatbot API locally

The local API requires Python 3.11+, [uv](https://docs.astral.sh/uv/), and a Groq API key.

```bash
uv sync
```

Create a `.env` file in the repository root with:

```dotenv
GROQ_API_KEY=your_groq_api_key
```

Then start the API:

```bash
uv run uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000/docs to test the API. The frontend is configured to call the deployed chatbot endpoint, so use the API docs or an HTTP client when testing the local API unless you also change `CHATBOT_API_URL` in `assets/js/main.js` and configure CORS.

## Deployment

RAG Chatbot API: [Hugging Face Space](https://huggingface.co/spaces/Rudra-G-23/rudra-portfolio-rag-chatbot-api/tree/main) & [API Docs](https://rudra-g-23-rudra-portfolio-rag-chatbot-api.hf.space/docs)

The FastAPI backend is hosted by Hugging Face Spaces. It uses Groq for text generation with the `openai/gpt-oss-20b` model; Hugging Face does not provide the LLM inference. Configure `GROQ_API_KEY` as a private Space secret. The browser calls only the public `/chat` endpoint, so no API token is included in the frontend.
