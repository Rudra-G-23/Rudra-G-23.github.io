import json
import os

from rich import print
from rich.traceback import install
from sentence_transformers import SentenceTransformer

install()

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

DATA_FOLDER = "chatbot-data"
OUTPUT_FILE = "chatbot-data/data.json"


def read_files(folder):
    texts = []

    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder, filename)

            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

                texts.append({"source": filename, "content": content})

    return texts


def chunk_text(text, chunk_size=150):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i : i + chunk_size])
        chunks.append(chunk)

    return chunks


def process_data():
    raw_data = read_files(DATA_FOLDER)
    final_data = []

    for item in raw_data:
        chunks = chunk_text(item["content"])

        for chunk in chunks:
            embedding = model.encode(chunk).tolist()

            final_data.append(
                {"text": chunk, "embedding": embedding, "source": item["source"]}
            )

    return final_data


def save_to_json(data):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    print("Creating embeddings...")
    data = process_data()
    save_to_json(data)
    print(f"Saved {len(data)} chunks to {OUTPUT_FILE}")
