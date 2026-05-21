import requests

headers = {
    "Authorization" : "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2IiwiZXhwIjoxNzc5NzI3NjE0fQ.6eqKkLZ9dOMT4rAMgk6U-et7zrlJem5qTFnsIfzcUtI"
}

requisicao = requests.get("http://127.0.0.1:8000/auth/refresh", headers=headers)
print(requisicao)
print(requisicao.json())

