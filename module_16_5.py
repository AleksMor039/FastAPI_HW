'''
Домашнее задание по теме "Шаблонизатор Jinjia2"
Цель: научиться взаимодействовать с шаблонами Jinja2
и использовать их в запросах.
Задача: "Список пользователей в шаблоне"
'''

from fastapi import FastAPI, Path, status, Body, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Annotated, List
from fastapi.templating import Jinja2Templates

# Создаём экземпляр приложения FastAPI
app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, debug=True)
# созд. объект Jj2Templates (папка шаблонов=templates)
templates = Jinja2Templates(directory="templates")


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


# 1.get запрос по маршруту "/"(ф-ия приним. арг.request и возвр. TempleResponse
@app.get("/", response_class=HTMLResponse)
async def get_main_page(request: Request) -> HTMLResponse:
    # TemplateResponse подкл.заготов. шаблон 'users.html', и передаёт в него request и список users.
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


# 2. get запрос по маршруту "/user/{user_id}"
@app.get("/user/{user_id}", response_class=HTMLResponse)
async def get_users(request: Request, user_id: Annotated[int, Path(ge=1)]) -> HTMLResponse:
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": users[user_id-1]})
    raise HTTPException(status_code=404, detail="User not found")



# 3. delete запрос по маршруту "/user/{user_id}"
@app.delete("/user/{user_id}")  # удаляет из списка users пользователя по user_id
async def delete_user(user_id: Annotated[int, Path(description="ID user")]) -> str:
    for i, user in enumerate(users):
        if user.id == user_id:
            del users[i]
            return f"User with number id {user_id} deleted"
    raise HTTPException(status_code=404, detail="User was not found")


# 3.post запрос по маршруту "/user/{username}/{age}"
@app.post("/user/{username}/{age}", response_model=User)
async def post_user(username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username",
                                                  pattern="^[а-яА-ЯёЁa-zA-Z\\S]+$")],
                    age: Annotated[int, Path(ge=18, le=120, description="Enter age")]) -> str:
    user_id = max((t.id for t in users), default=0) + 1  # id этого объекта будет на 1 больше,
    # чем у последнего в списке users. Если список users пустой, то 1.
    new_user = User(id=user_id, username=username, age=age)  # Все ост. парам. объекта User - переданные
    # в функцию username и age соответственно.
    users.append(new_user)  # Добавляет в список users объект User.
    return new_user  # возвращает созданного пользователя.


# 4. put запрос по маршруту "/user/{user_id}/{username}/{age}"
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
