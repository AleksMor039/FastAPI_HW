from fastapi import FastAPI

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
async def User_Number(user_id: int) -> dict:
    return {"message": f"Вы вошли как пользователь № {user_id}"}


# маршрут к страницам пользователей по "/user"
@app.get("/user")
async def User_Info(username: str, age: int) -> dict:
    return {"message": f"Информация о пользователе. Имя:{username}, Возраст:{age}"}
