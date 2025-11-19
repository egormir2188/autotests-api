import httpx


# response = httpx.get('https://jsonplaceholder.typicode.com/todos/1')
#
# print(response.status_code)
# print(response.json())
#
# data = {
#     'userId': 1,
#     'title': 'New task',
#     'completed': False
# }
#
# response = httpx.post('https://jsonplaceholder.typicode.com/todos', json = data)
#
# print(response.status_code)
# print(response.json())
# print(response.request.headers)

# data = {"username": "test_user34", "password": "1234563"}
# response = httpx.post("https://httpbin.org/post", data = data)
#
# print(response.status_code)
# print(response.json())
# print(response.request.headers)

# headers = {"Authorization": "Bearer token"}
# response = httpx.post("https://httpbin.org/post", headers = headers)
#
# print(response.request.headers)
# print(response.json())

# params = {'userId': 1}
# response = httpx.get('https://jsonplaceholder.typicode.com/todos?userId=1', params = params)
# print(response.url)
# print(response.json())

# files = {"file": ("example.txt", open("example.txt", "rb"))}
# response = httpx.post("https://httpbin.org/post", files=files)
#
# print(response.json())

try:
    response = httpx.get("https://jsonplaceholder.typicode.com/invalid-url")
    response.raise_for_status()  # Вызовет исключение при 4xx/5xx
except httpx.HTTPStatusError as e:
    print(f"Ошибка запроса: {e}")

try:
    response = httpx.get("https://httpbin.org/delay/5", timeout=2)
except httpx.ReadTimeout:
    print("Запрос превысил лимит времени")