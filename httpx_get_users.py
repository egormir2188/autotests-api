import httpx

from tools.fakers import get_random_email


payload = {
    "email": get_random_email(),
    "password": "string",
    "lastName": "string",
    "firstName": "string",
    "middleName": "string"
}
url = 'http://localhost:8000'
response = httpx.post(f'{url}/api/v1/users', json=payload)

print(response.status_code, response.json(), sep = '\n')