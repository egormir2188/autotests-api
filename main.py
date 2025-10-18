import json

json_data = '{"name": "Иван", "age": 30, "is_student": false}'
# парсинг (преобразорвание json строки в словарь)
parsed_data = json.loads(json_data)

# сериализация - преобразование python объекта в json строку
data = {
    "name": "Мария",
    "age": 25,
    "is_student": True
}

json_string = json.dumps(data, indent=4)

# чтение из json
with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    print(data)

# запись оыщт в файл
with open("data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)
