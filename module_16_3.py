'''
Домашнее задание по теме "CRUD Запросы:
Get, Post, Put Delete.
'''

from fastapi import FastAPI, Path, HTTPException
from typing import Annotated

# Создаём экземпляр приложения FastAPI
app = FastAPI()
# создаём словарь
users = {'1': 'Имя: Example, возраст:18'}

'''
Реализация 4-х CRUD запросов:
'''


# 1.get запрос по маршруту "/users"
@app.get("/users")
async def get_users() -> dict:
    return users


# 2.post запрос по маршруту "/user/{username}/{age}"
@app.post("/user/{username}/{age}")
async def post_users(username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username",
                                                   pattern="^[а-яА-ЯёЁa-zA-Z\\S]+$")],
                     age: Annotated[int, Path(ge=18, le=120, description="Enter age")]) -> str:
    new_user = str(int(max(users, key=int)) + 1)
    users[new_user] = f"Имя: {username}, возраст: {age}"
    return f"User {new_user} is registered"


# 3. put запрос по маршруту "/user/{user_id}/{username}/{age}"
@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: Annotated[int, Path(gt=0, description="Enter user_id")],
                      username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username",
                                                    pattern="^[а-яА-ЯёЁa-zA-Z\\S]+$")],
                      age: Annotated[int, Path(ge=18, le=120, description="Enter age")]) -> str:
    users[user_id] = f"Имя: {username}, возраст: {age}"
    return f"User {user_id} has been updated"


# 4. delete запрос по маршруту "/user/{user_id}"
@app.delete("/user/{user_id}")
async def delete_user(user_id: Annotated[str, Path(description="ID user")]) -> str:
    if user_id not in users:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    del users[user_id]
    return f"User {user_id} has been deleted"
