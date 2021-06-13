from os import replace
from starlette.responses import JSONResponse
from pydantic import BaseModel
import matplotlib.pyplot as plt
import shutil
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Optional
from recom_client_api.client_api import Client
from recom_client_api.api_requests.user_api import GetUserValues
import requests
import base64

router = APIRouter()
templates = Jinja2Templates(directory="templates")
client = Client()

src_result = "static/public/anh-tach-nen/"

data = {
    "id_ao": None,
    "category_ao": None,
    "id_quan": None,
    "category_quan": None,
    "body": 4985
    }

cache_DRESS = []
cache_TOP = []
cache_PANTS = []
cache_SKIRT = []



def convert_to_file(result_image):
    pass
  

#SIZE FITTING
@router.get("/products", response_class=HTMLResponse)
async def api_fitsize(request: Request):
    """
    Recommend size with each category with input size charts and body measurement
    """
    return templates.TemplateResponse("inner-page-fix.html",{"request":request})

@router.get("/predict", response_class=JSONResponse)
async def api_findsize(request: Request):
    """
    Recommend size using data and Deep learning
    """
    return templates.TemplateResponse("index.html", {"request":request})

#TRY ON
@router.get("/tryon", response_class=HTMLResponse)
async def tryon_page(request: Request):
    return templates.TemplateResponse("tryon.html",{"request":request})



@router.get("/result")
async def api_get_result_tryon(iid:str, category:str, request: Request):
    """
    with each certain pants or shirt, proceed to try on the mannequin and return, display image to UI 
    """
    category = category.split("-")
    cat = category[0]
    value = category[1].replace(" ","_")

    if cat == "DRESS":
        data["id_ao"] = iid
        data["category_ao"] = value
        data["id_quan"] = iid
        data["category_quan"] = value

    elif cat == "TOP":
        data["id_ao"] = iid
        data["category_ao"] = value
        if cache_PANTS == [] or cache_SKIRT == []:
            #image = plt.imread(src_result + "Top/IMG_{}.png".format(iid))
            shutil.copy(src_result + "Top/IMG_{}.png".format(iid),src_result + "result.png") 

    elif cat == "PANTS":
        data["id_quan"] = iid
        data["category_quan"] = value
        if cache_PANTS == []:
            shutil.copy(src_result + "Pants/IMG_{}.png".format(iid),src_result + "result.png")
        cache_PANTS.append(data["id_quan"])

    elif cat == "SKIRT":
        data["id_quan"] = iid
        data["category_quan"] = value
        if cache_SKIRT == []:
            shutil.copy(src_result + "Skirt/IMG_{}.png".format(iid),src_result + "result.png")
        cache_SKIRT.append(data["id_quan"])
    url = "http://192.168.50.69:5849/{}/{}/{}/{}/{}".format(data["id_ao"],data["category_ao"],data["id_quan"],data["category_quan"],data["body"])
    print(url)
    # response = requests.get(url="http://192.168.50.69:5849/4990/trousers/5013/long_sleeve_top/4985")
    # result = response.content
    # image = base64.b64decode(result.content)
    # filename = 'static/public/anh-tach-nen//image.png'
    
    # with open(filename, 'wb') as f:
    #      f.write(image)

    message = "DONE!"
    return templates.TemplateResponse("tryon.html",{"request":request,"message":message})