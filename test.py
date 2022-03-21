import requests

data = {
    "username": "johndoe",
    "password": "hello",
}
res = requests.post('http://localhost:8000/auth/token', data=data).json()
access_token = res['access_token']

annotation = requests.get("http://localhost:8000/images/annotations/1/1",
                         headers={'Authorization': 'Bearer ' + access_token})

print(annotation.text)
