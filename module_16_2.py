from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()


# маршрут к главной странице
@app.get("/")
async def Main_page() -> dict:
    return {"message": "Главная страница"}


# маршрут к странице администратора
@app.get("/user/admin")
async def Admin_page() -> dict:
    return {"message": "Вы вошли как администратор"}


# маршрут к страницам пользователей по "/user/{user_id}
@app.get("/user/{user_id}")
async def User_Number(
        user_id: Annotated[int, Path(ge=1,
                                      le=100,
                                      description="Enter User ID")]
) -> dict:
    return {"message": f"Вы вошли как пользователь № {user_id}"}


# маршрут к страницам пользователей по "/user"
@app.get("/user/{username}/{age}")
async def User_Info(
        username: Annotated[str, Path(min_length=5,
                                       max_length=20,
                                       regex="^[A-Za-z\\S]+$",
                                       description = "Enter username")],
        age: Annotated[int, Path(ge=18,
                                  le=120,
                                  description = "Enter age")],
) -> dict:
    return {"message": f"Информация о пользователе. Имя:{username}, Возраст:{age}"}
