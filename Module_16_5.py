# Домашнее задание по теме "Шаблонизатор Jinja 2."
# *****************************************************************************************************************
# Исользуются
#   Python версии 3.11.7
#
# Задача "Список пользователей в шаблоне":
#
# Подготовка:
#   1. Используйте код из предыдущей задачи.
#   2. Скачайте заготовленные шаблоны для их дополнения.
#   3. Шаблоны оставьте в папке templates у себя в проекте.
#   4. Создайте объект Jinja2Templates, указав в качестве папки шаблонов - templates.
#
# Измените и дополните ранее описанные CRUD запросы:
#
# Напишите новый запрос по маршруту '/':
#   1. Функция по этому запросу должна принимать аргумент request и возвращать TemplateResponse.
#   2. TemplateResponse должен подключать ранее заготовленный шаблон 'users.html', а также передавать в него
#   2. request и список users. Ключи в словаре для передачи определите самостоятельно в соответствии с шаблоном.
#
# Измените get запрос по маршруту '/user' на '/user/{user_id}':
#   1. Функция по этому запросу теперь принимает аргумент request и user_id.
#   2. Вместо возврата объекта модели User, теперь возвращается объект TemplateResponse.
#   3. TemplateResponse должен подключать ранее заготовленный шаблон 'users.html', а также передавать в него
#      request и одного из пользователей - user. Ключи в словаре для передачи определите самостоятельно
#      в соответствии с шаблоном.
#
# Создайте несколько пользователей при помощи post запроса со следующими данными:
#   1. username - UrbanUser, age - 24
#   2. username - UrbanTest, age - 22
#   3. username - Capybara, age - 60
#
# В шаблоне 'users.html' заготовлены все необходимые теги и обработка условий, вам остаётся только дополнить
# закомментированные строки вашим Jinja 2 кодом (использование полей id, username и age объектов модели User):
#   1. По маршруту '/' должен отображаться шаблон 'users.html' со списком все ранее созданных объектов$
#   2. Здесь каждая из записей является ссылкой на описание объекта, информация о котором отображается
#      по маршруту '/user/{user_id}':
#
# *****************************************************************************************************************

from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated, List
from pydantic import BaseModel


# Создаем экземпляр приложения FastAPI
app = FastAPI()
templates = Jinja2Templates(directory='templates')

users = []

class User(BaseModel):
    id: int = None
    username: str
    age: int

# Определение базового маршрута
@app.get('/')
def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html',{'request': request, 'users': users})

# Запрос на получение всех пользователей
@app.get('/users')
def get_users() -> List[User]:
    return users

# Запрос на получение пользователя по id
@app.get('/user/{user_id}')
def get_user(request: Request, user_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse('users.html', {'request':request, 'user': users[user_id-1]})
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")

# Запрос на добавление пользователя
@app.post('/user/{username}/{age}')
async def create_user(username: Annotated[str, Path(..., min_length=5, max_length=20, description="Enter username", examples="UrbanUser")],
                      age: Annotated[int, Path(..., ge=18, le=120, description="Enter age", examples=24)]) -> User:

    if len(users) != 0:
        new_id = len(users) + 1
    else:
        new_id = 1

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

# uvicorn Module_16_5:app --reload
