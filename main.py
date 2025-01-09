from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
from pathlib import Path
from model import FormData
from auth import router as auth_router 

app = FastAPI()


JSON_FILE = 'data.json'

# Настройка шаблонов и статических файлов
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router, prefix="/auth", tags=["auth"])

# Главная страница
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/form", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


def save_order_to_json(order: dict):
    try:
        try:
            with open(JSON_FILE, "r", encoding="utf-8") as file:
                orders = json.load(file)
        except FileNotFoundError:
            orders = []  
        # Добавление нового заказа
        orders.append(order) 
        # Запись обратно в файл
        with open(JSON_FILE, "w", encoding="utf-8") as file:
            json.dump(orders, file, ensure_ascii=False, indent=4)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сохранения заказа: {e}")


@app.post("/reserve")
async def reserve(request: Request):
    try:
        data = await request.json()

        required_fields = ["name", "email", "date", "time", "duration", "station"]
        if not all(field in data for field in required_fields):
            raise HTTPException(status_code=400, detail="Не все поля заполнены")

        
        save_order_to_json(data)
        return {"message": "Заказ успешно оформлен!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка: {e}")


@app.get("/item", response_class=HTMLResponse)
async def item_page(request: Request):
    return templates.TemplateResponse("item.html", {"request": request})
