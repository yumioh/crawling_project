import requests

#fast api 테스트
response = requests.get("http://127.0.0.1:8000/items/foo")
print(response.text)