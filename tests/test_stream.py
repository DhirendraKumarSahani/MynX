import requests

url = "http://127.0.0.1:8000/api/v1/chat/stream"

data = {
    "query": "Explain machine learning",
    "thread_id": "1"
}

response = requests.post(url, json=data, stream=True)

print("Status:", response.status_code)

for chunk in response.iter_lines():
    if chunk:
        text = chunk.decode().replace("data: ", "")
        print(text)