import requests

url = "https://special-hound-devoted.ngrok-free.app/analyze"
data = {"process": "perplexity.ai"}

response = requests.post(url, json=data)
print(response.json())
