Portfolio Live Link: https://rudra-g-23.github.io/

RAG Chatbot API: [Hugging Face Space](https://huggingface.co/spaces/Rudra-G-23/rudra-portfolio-rag-chatbot-api/tree/main) & [API Docs](https://rudra-g-23-rudra-portfolio-rag-chatbot-api.hf.space/docs)

The FastAPI backend is hosted by Hugging Face Spaces. It uses Groq for text generation with the `openai/gpt-oss-20b` model; Hugging Face does not provide the LLM inference. Configure `GROQ_API_KEY` as a private Space secret. The browser calls only the public `/chat` endpoint, so no API token is included in the frontend.
