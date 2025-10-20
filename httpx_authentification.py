import httpx



url = 'http://localhost:8000'
login_payload = {
    "email": "egormir@mail.ru",
    "password": "test"
}

login_response = httpx.post(f'{url}/api/v1/authentication/login', json=login_payload)
login_response_data = login_response.json()

print(f'Login response: {login_response_data}', f'Status code: {login_response.status_code}', sep = '\n')

refresh_payload = {
    'refreshToken': login_response_data['token']['refreshToken']
}

refresh_response = httpx.post(f'{url}/api/v1/authentication/refresh', json=refresh_payload)
refresh_response_data = refresh_response.json()

print(f'Refresh response: {refresh_response_data}', f'Status code: {refresh_response.status_code}', sep = '\n')