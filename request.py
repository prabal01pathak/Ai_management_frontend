import requests

server_url = 'http://localhost:8000'

form_data = {
    'username': 'johndoe',
    'password': 'hell',
}
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

response = requests.post(server_url + '/auth/token', data=form_data, headers=headers)
response_json = response.json()
print(response.status_code)
print(response_json['access_token'])
