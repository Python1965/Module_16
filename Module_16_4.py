# Домашнее задание по теме "Модели данных Pydantic"
# *****************************************************************************************************************
# Исользуются
#   Python версии 3.11.7
#
# Задача "Модель пользователя":
#
# Используйте CRUD запросы из предыдущей задачи.
# Создайте пустой список users = []
# Создайте класс(модель) User, наследованный от BaseModel, который будет содержать следующие поля:
#
#   1. id - номер пользователя (int)
#   2. username - имя пользователя (str)
#   3. age - возраст пользователя (int)
#
# Измените и дополните ранее описанные 4 CRUD запроса:
#   get запрос по маршруту '/users' теперь возвращает список users.
#   post запрос по маршруту '/user/{username}/{age}', теперь:
#       1. Добавляет в список users объект User.
#       2. id этого объекта будет на 1 больше, чем у последнего в списке users. Если список users пустой, то 1.
#       3. Все остальные параметры объекта User - переданные в функцию username и age соответственно.
#       4. В конце возвращает созданного пользователя.
#
#   put запрос по маршруту '/user/{user_id}/{username}/{age}' теперь:
#       1. Обновляет username и age пользователя, если пользователь с таким user_id есть в списке users
#          и возвращает его.
#       2. В случае отсутствия пользователя выбрасывается исключение HTTPException с описанием
#          "User was not found" и кодом 404.

#   delete запрос по маршруту '/user/{user_id}', теперь:
#       1. Удаляет пользователя, если пользователь с таким user_id есть в списке users и возвращает его.
#       2. В случае отсутствия пользователя выбрасывается исключение
#          HTTPException с описанием "User was not found" и кодом 404.
#
# *****************************************************************************************************************

from fastapi import FastAPI, Path, status, Body, HTTPException
from typing import Annotated, List
from pydantic import BaseModel


# Создаем экземпляр приложения FastAPI
app = FastAPI()

users = []

class User(BaseModel):
    id: int = None
    username: str
    age: int

# Определение базового маршрута
@app.get("/")
async def root() -> dict:
    return {"message": "Главная страница"}

# Запрос на получение всех пользователей
@app.get('/users')
def get_users() -> List[User]:
    return users

# Запрос на добавление пользователя
@app.post('/user/{username}/{age}')
async def create_user(username: Annotated[str, Path(..., min_length=5, max_length=20, description="Enter username", examples="UrbanUser")],
                      age: Annotated[int, Path(..., ge=18, le=120, description="Enter age", examples=24)]) -> User:

    new_id = (users[-1].id + 1) if users else 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user


# Запрос на изменение данных пользователя
@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: Annotated[int, Path(..., ge=1, le=100, title="User ID", description="Enter User ID", examples=1)],
                      username: Annotated[str, Path(..., min_length=5, max_length=20, description="Enter username", examples="UrbanUser")],
                      age: Annotated[int, Path(..., ge=18, le=120, description="Enter age", examples=24)]) -> User:

    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    else:
        raise HTTPException(status_code=404, detail='Пользователя не существует')


# Запрос на удаление конкретного пользователя
@app.delete('/user/{user_id}')
async def delete_user(user_id: Annotated[int, Path(..., ge=1, le=100, title="User ID", description="Enter User ID", examples=1)]) -> User:

    for i, user in enumerate(users):
        if user.id == user_id:
            return users.pop(i)
    else:
        raise HTTPException(status_code=404, detail='Пользователя не существует')



#uvicorn Module_16_4:app --reload
