import httpx

url = 'http://localhost:8000/'
payload = {
    "email": "egormir@mail.ru",
    "password": "test"
}

response_login = httpx.post(f'{url}api/v1/authentication/login', json=payload)
token = response_login.json()['token']['accessToken']

response_me = httpx.get(f'{url}api/v1/users/me', headers={'Authorization': f'Bearer {token}'})

print(response_me.json(), response_me.status_code, sep = '\n')