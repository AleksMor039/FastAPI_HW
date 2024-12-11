'''
Домашнее задание по теме "Модели данных Pydantic:
Цель: научиться описывать и исп. Pydantic модель.
'''

from fastapi import FastAPI, Path, status, Body, HTTPException
from pydantic import BaseModel
from typing import List
from typing import Annotated

# Создаём экземпляр приложения FastAPI
app = FastAPI()

# Создаём класс(модель) User, наслед. от BaseModel
class User(BaseModel):
    id: int
    username: str
    age: int

# создаём пустой список
users: List[User] = []
'''
Изменение и дополнение ранее описанных 4-х CRUD запросов:
'''

# 1.get запрос по маршруту "/users"
@app.get("/users", response_model=List[User])
async def get_users() -> list:
    return users

# 2.post запрос по маршруту "/user/{username}/{age}"
@app.post("/user/{username}/{age}", response_model=User)
async def post_users(username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username",
                                                   pattern="^[а-яА-ЯёЁa-zA-Z\\S]+$")],
                     age: Annotated[int, Path(ge=18, le=120, description="Enter age")]) -> str:
    user_id = max((t.id for t in users), default=0) + 1  # id этого объекта будет на 1 больше,
    # чем у последнего в списке users. Если список users пустой, то 1.
    new_user = User(id=user_id, username=username, age=age)  # Все ост. парам. объекта User - переданные
    # в функцию username и age соответственно.
    users.append(new_user)  # Добавляет в список users объект User.
    return new_user  # возвращает созданного пользователя.

# 3. put запрос по маршруту "/user/{user_id}/{username}/{age}"
@app.put("/user/{user_id}/{username}/{age}", response_model=User)
async def update_user(user_id: Annotated[int, Path(gt=0, description="Enter user_id")],
                      username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username",
                                                    pattern="^[а-яА-ЯёЁa-zA-Z\\S]+$")],
                      age: Annotated[int, Path(ge=18, le=120, description="Enter age")]) -> User:
# Обнов. username и age пользов., если пользов. с таким user_id есть в списке users и возвр. его.
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")

# 4. delete запрос по маршруту "/user/{user_id}"
@app.delete("/user/{user_id}")  # удаляет из списка users пользователя по user_id
async def delete_user(user_id: Annotated[int, Path(description="ID user")]) -> str:
    for i, user in enumerate(users):
        if user.id == user_id:
            del users[i]
            return "User deleted"
    raise HTTPException(status_code=404, detail="User was not found")
