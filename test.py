import requests

data = {
    "username": "johndoe",
    "password": "hello",
}
res = requests.post('http://localhost:8000/auth/token', data=data).json()
access_token = res['access_token']

project = requests.get("http://localhost:8000/images/1",
                         headers={'Authorization': 'Bearer ' + access_token})

image = requests.get("http://localhost:8000/images/1/1",
                         headers={'Authorization': 'Bearer ' + access_token})


print(image.text)
