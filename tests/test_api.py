import requests

url = "http://127.0.0.1:8000/chat"

while True:
    question = input("Ask:")

    res = requests.post(url, json={"question": question})

    print("\nAnswer:\n", res.json()["answer"])
    print("-" * 50)