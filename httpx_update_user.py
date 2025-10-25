import httpx

from tools.fakers import fake

url = 'http://localhost:8000'

create_user_payload = {
    "email": fake.email(),
    "password": "string",
    "lastName": "string",
    "firstName": "string",
    "middleName": "string"
}

create_user_response = httpx.post(f'{url}/api/v1/users', json=create_user_payload)
create_user_response_data = create_user_response.json()

print('Create user data:', create_user_response_data)

login_payload = {
    "email": create_user_payload["email"],
    "password": create_user_payload["password"]
}

login_response = httpx.post(f'{url}/api/v1/authentication/login', json=login_payload)
login_response_data = login_response.json()

print('Login data:', login_response_data)

update_user_payload = {
    "email": fake.email(),
    "lastName": "string",
    "firstName": "string",
    "middleName": "string"
}

update_user_headers = {
    "Authorization": f'Bearer {login_response_data["token"]["accessToken"]}'
}

update_user_response = httpx.patch(
    f'{url}/api/v1/users/{create_user_response_data["user"]["id"]}', json=update_user_payload,
    headers=update_user_headers
)
update_user_response_data = update_user_response.json()

print(f'Update user data: {update_user_response_data}', f'Status code: {update_user_response.status_code}', sep = '\n')