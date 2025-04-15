import requests

res = requests.post("http://localhost:8000/completion", json={
    "prompt": "What is the capital of France?",
    "n_predict": 50
})

print(res.json())
