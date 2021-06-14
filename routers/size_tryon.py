import shutil
from typing import Optional
import requests
import base64

from os import replace
from fastapi import APIRouter
from fastapi import Request
from database.db import ItemTryon
from database.db import UserDB, ItemDB
from fastapi.responses import   FileResponse, HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from recom_client_api.client_api import Client



router = APIRouter()
templates = Jinja2Templates(directory="templates")
client = Client()
it = ItemDB()

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
async def api_get_result_tryon(iid:str, category: str , request: Request):
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

    url = "http://192.168.50.69:5849/{}/{}/{}/{}/{}".format(data["id_quan"],data["category_quan"],data["id_ao"],data["category_ao"],data["body"])
    print(url)
    response = requests.get(url=url)
    result = response.content
    image = base64.b64decode(result)
    filename = 'static/public/anh-tach-nen/image.png'
    
    with open(filename, 'wb') as f:
        f.write(image)

    message = "DONE!"
    return templates.TemplateResponse("tryon.html",{"request":request,"message":message})

@router.post("/tryon_stateless")
async def api_get_result_main(items:ItemTryon):
    
    if items.iid_ao == None and items.iid_quan == None:
        #TODO: return canh mac quan ao mac dinh
        pass
    
    if items.iid_ao == None and items.iid_quan != None:
        #TODO: return canh mac iid_quan va ao mac dinh
        pass

    if items.iid_ao != None and items.iid_quan == None:
        #TODO: return canh mac iid_ao va quan mac dinh
        pass

    if items.iid_ao != None and items.iid_quan != None:
        #TODO: return canh mac iid_ao va iid_quan
        info_iid_ao = it.get_item_info(items.iid_ao)
        info_iid_quan = it.get_item_info(items.iid_quan)
        url = "http://192.168.50.69:5849/{}/{}/{}/{}/{}".format(items.iid_quan, info_iid_quan["category"], items.iid_ao, info_iid_ao["category"], 4985)
        response = requests.get(url=url)
        result = response.content
        image = base64.b64decode(result)
        return FileResponse(image,media_type="image/png")
