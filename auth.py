from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr
import json
import bcrypt

# Конфигурация
USER_DB_FILE = "users.json"
router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Загрузка и сохранение пользователей
def load_users():
    try:
        with open(USER_DB_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open(USER_DB_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=4)

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

# Маршрут для отображения страницы регистрации
@router.get("/register", response_class=HTMLResponse)
async def show_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# Маршрут для обработки данных формы регистрации
@router.post("/register")
async def register(
    username: str = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...),
):
    users = load_users()

    # Проверка существующего пользователя
    if username in users:
        raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")

    # Хэшируем пароль и сохраняем пользователя
    hashed_password = hash_password(password)
    users[username] = {"email": email, "hashed_password": hashed_password}
    save_users(users)

    return {"message": "Пользователь успешно зарегистрирован"}
