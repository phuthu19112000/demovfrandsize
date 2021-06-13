from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Form
from routers import items, users, size_tryon
#from routers import size_tryon

# https://github.com/abhishekkumaribt/recommend-clothing-size/blob/master/code.py
# https://ichi.pro/vi/bat-dau-voi-fastapi-bang-python-146061885479055
# https://ichi.pro/vi/xay-dung-api-nhanh-chong-bang-fastapi-va-python-255341594090036

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"),name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(items.router)
app.include_router(users.router)
app.include_router(size_tryon.router)

@app.get("/",response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("home.html",{"request":request})