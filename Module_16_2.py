# Домашнее задание по теме "Валидация данных".
# *****************************************************************************************************************
# Исользуются
#   Python версии 3.11.7
#
# Задача "Аннотация и валидация":
#
# Допишите валидацию для маршрутов из предыдущей задачи при помощи классов Path и Annotated:
# '/user/{user_id}' - функция, выполняемая по этому маршруту, принимает аргумент user_id,
# для которого необходимо написать следующую валидацию:
#
#   1. Должно быть целым числом
#   2. Ограничено по значению: больше или равно 1 и меньше либо равно 100.
#   3. Описание - 'Enter User ID'
#   4. Пример - '1' (можете подставить свой пример не противоречащий валидации)
#
# '/user' замените на '/user/{username}/{age}' - функция, выполняемая по этому маршруту,
# принимает аргументы username и age, для которых необходимо написать следующую валидацию:
#
#   1. username - строка, age - целое число.
#   2. username ограничение по длине: больше или равно 5 и меньше либо равно 20.
#   3. age ограничение по значению: больше или равно 18 и меньше либо равно 120.
#   4. Описания для username и age - 'Enter username' и 'Enter age' соответственно.
#   5. Примеры для username и age - 'UrbanUser' и '24' соответственно.
#      (можете подставить свои примеры не противоречащие валидации).
#
# Примечание
#   Если у вас не отображаются параметры Path, проверьте, сделали вы присвоение данных или подсказку типа.
#   Верно: username: Annotated[...]. Не верно: username = Annotated[...]
## *****************************************************************************************************************

from fastapi import FastAPI, Path
from typing import Annotated

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
#async def get_user_data(username: str, age: int) -> dict:
async def get_user_data(username: Annotated[str, Path(..., min_length=5, max_length=20, description="Enter username")],
                        age: Annotated[int, Path(..., ge=18, le=120, description="Enter age")]) -> dict:
    return {"Имя": username, "Возраст": age}


@app.get("/user/{user_id}")
async def get_user(user_id: Annotated[int, Path(..., ge=1, le=100, title="User ID", description="Enter User ID")]) -> dict:
    return {"user_id": f"Вы вошли как пользователь № {user_id}"}


#uvicorn Module_16_2:app --reload
