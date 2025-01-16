# Домашнее задание по теме "Основы Fast Api и маршрутизация"
# *****************************************************************************************************************
# Исользуются
#   Python версии 3.11.7
#
# Задача "Начало пути":
# Подготовка:
# Установите фреймворк FastAPI при помощи пакетного менеджера pip. Версию Python можете выбрать
# самостоятельно (3.9 - 3.12).
#
# Маршрутизация:
#   1. Создайте приложение(объект) FastAPI предварительно импортировав класс для него.
#   2. Создайте маршрут к главной странице - "/". По нему должно выводиться сообщение "Главная страница".
#   3. Создайте маршрут к странице администратора - "/user/admin". По нему должно выводиться сообщение
#      "Вы вошли как администратор".
#   4. Создайте маршрут к страницам пользователей используя параметр в пути - "/user/{user_id}".
#      По нему должно выводиться сообщение "Вы вошли как пользователь № <user_id>".
#   5. Создайте маршрут к страницам пользователей передавая данные в адресной строке - "/user".
#      По нему должно выводиться сообщение "Информация о пользователе. Имя: <username>, Возраст: <age>".
#
# Примечание
#   1. Все маршруты пишутся при мощи GET запроса.
#   2. Помните о важности порядка записи запросов в вашем файле.
#   3. Названия функций можете придумать самостоятельно с учётом логики прописанной в них.
## *****************************************************************************************************************

from fastapi import FastAPI

# Создаем экземпляр приложения FastAPI
app = FastAPI()

# Определение базового маршрута
@app.get("/")
async def root() -> str:
    return "Главная страница"

@app.get("/user/admin")
async def get_admin() -> str:
    return "Вы вошли как администратор"

@app.get("/user/{user_id}")
async def get_user(user_id: str) -> str:
    return "Вы вошли как пользователь № " + user_id

@app.get("/user")
async def get_user_data(username: str, age: str) -> str:
    return f"Информация о пользователе. Имя: '{username}', Возраст: {age}."

# uvicorn Module_16_1:app --reload