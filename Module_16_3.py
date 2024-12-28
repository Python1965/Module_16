# Домашнее задание по теме "CRUD Запросы: Get, Post, Put Delete."
# *****************************************************************************************************************
# Исользуются
#   Python версии 3.11.7
#
# Задача "Имитация работы с БД":
#
# Создайте новое приложение FastAPI и сделайте CRUD запросы.
# Создайте словарь users = {'1': 'Имя: Example, возраст: 18'}
#
# Реализуйте 4 CRUD запроса:
#
#   1. get запрос по маршруту '/users', который возвращает словарь users.
#   2. post запрос по маршруту '/user/{username}/{age}', который добавляет в словарь
#      по максимальному по значению ключом значение строки "Имя: {username}, возраст: {age}".
#      И возвращает строку "User <user_id> is registered".
#   3. put запрос по маршруту '/user/{user_id}/{username}/{age}', который обновляет значение из словаря users
#      под ключом user_id на строку "Имя: {username}, возраст: {age}". И возвращает строку "The user <user_id> is updated"
#   4. delete запрос по маршруту '/user/{user_id}', который удаляет из словаря users по ключу user_id пару.
#
# Выполните каждый из этих запросов по порядку. Ответы должны совпадать:
#   1. GET '/users'
#       {
#       "1": "Имя: Example, возраст: 18"
#       }
#
#   2. POST '/user/{username}/{age}' # username - UrbanUser, age - 24
#       "User 2 is registered"
#
#   3. POST '/user/{username}/{age}' # username - NewUser, age - 22
#       "User 3 is registered"
#
#   4. PUT '/user/{user_id}/{username}/{age}' # user_id - 1, username - UrbanProfi, age - 28
#       "User 1 has been updated"
#
#   5. DELETE '/user/{user_id}' # user_id - 2
#       "User 2 has been deleted"
#
#   6. GET '/users'
#       {
#       "1": "Имя: UrbanProfi, возраст: 28",
#       "3": "Имя: NewUser, возраст: 22"
#       }
#
# *****************************************************************************************************************


from fastapi import FastAPI, Path
from typing import Annotated


users_db = {1: {"Имя": "Example", "возраст": 18}}

# Создаем экземпляр приложения FastAPI
app = FastAPI()

# Определение базового маршрута
@app.get("/")
async def root() -> dict:
    return {"message": "Главная страница"}


@app.get("/user/admin")
async def get_admin() -> dict:
    return {"message": "Вы вошли как администратор"}


@app.get("/user/{username}/{age}")
async def get_user_data(username: Annotated[str, Path(..., min_length=5, max_length=20, description="Enter username", examples="UrbanUser")],
                        age: Annotated[int, Path(..., ge=18, le=120, description="Enter age", examples=24)]) -> dict:
    return {"Имя": username, "Возраст": age}


@app.get("/user/{user_id}")
async def get_user(user_id: Annotated[int, Path(..., ge=1, le=100, title="User ID", description="Enter User ID", examples=1)]) -> dict:
    return {"user_id": f"Вы вошли как пользователь № {user_id}"}


@app.get("/users")
async def get_users() -> dict:
    return users_db


@app.post('/user/{username}/{age}')
async def create_user(username: Annotated[str, Path(..., min_length=5, max_length=20, description="Enter username", examples="UrbanUser")],
                      age: Annotated[int, Path(..., ge=18, le=120, description="Enter age", examples=24)]) -> str:

    curr_ind = max(users_db, key=int) + 1
    users_db[curr_ind] = {"Имя": username, "возраст": age}
    return f"User {curr_ind} is registered"


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: Annotated[int, Path(..., ge=1, le=100, title="User ID", description="Enter User ID", examples=1)],
                      username: Annotated[str, Path(..., min_length=5, max_length=20, description="Enter username", examples="UrbanUser")],
                      age: Annotated[int, Path(..., ge=18, le=120, description="Enter age", examples=24)]) -> str:

    users_db[user_id] = {"Имя": username, "возраст": age}
    return f"User {user_id} has been updated"


@app.delete('/user/{user_id}')
async def update_user(user_id: Annotated[int, Path(..., ge=1, le=100, title="User ID", description="Enter User ID", examples=1)]) -> str:

    users_db.pop(user_id)
    return  f"User {user_id} has been deleted"



#uvicorn Module_16_3:app --reload
