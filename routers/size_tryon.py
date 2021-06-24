import requests
import base64
import json
from os import replace
from fastapi import Query
from fastapi import status
from typing import Optional
from fastapi import APIRouter
from fastapi import Request
from database.db import ItemDB
from fastapi import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from recom_client_api.client_api import Client
from size_recommendation.fit_size_op2 import Fit_size
from recom_client_api.api_requests.user_api import GetValues
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse


router = APIRouter()
templates = Jinja2Templates(directory="templates")
client = Client()
it = ItemDB()
dress_dict = [4978,4991,4993,4998,5002,5004,5005,5016]
src_result = "static/public/anh-tach-nen/"
filename = 'static/public/anh-tach-nen/image.png'

#SIZE FITTING
@router.get("/products", response_class=HTMLResponse)
async def api_fitsize(request: Request):
    """
    Recommend size with each category with input size charts and body measurement
    """
    return templates.TemplateResponse("inner-page-fix.html",{"request":request})


@router.get("/predict", response_class=HTMLResponse)
async def api_findsize(request: Request):
    """
    Recommend size using data and Deep learning
    """
    return templates.TemplateResponse("index.html", {"request":request})

@router.get("/fitsizecat", response_class=JSONResponse)
async def caculate_size(uid: int, category: str):
    # uid = uid.encode("windows-1252").decode("utf-8")
    # category = category.encode("windows-1252").decode("utf-8")
    instance = Fit_size(uid,category)
    info_user = await instance.get_info_uid()
    if info_user:
        size = instance.fit_size_female(info_user)
        code = status.HTTP_200_OK
        return {"code": code,"best size": size}
    elif info_user==None:
        code = status.HTTP_404_NOT_FOUND
        return {"code":code}

#TRY ON
@router.get("/tryon", response_class=HTMLResponse)
async def tryon_page(request: Request):
    return templates.TemplateResponse("tryon-fix.html",{"request":request})

@router.get("/result", response_description = "Try on Success")
async def api_get_result_tryon(iid_ao: Optional[str]= Query("5010",\
                               title = "id_ao must be a string",max_length=10),\
                               iid_quan: Optional[str]= Query("4990", \
                               title = "id_quan must be a string",max_length=10),\
                               in_or_out : Optional[int] = Query(0,\
                               title = "option for clothes")):
    
    data = {
    "mannequinPng": "/home/edso/Documents/nguyen/libigl/tutorial/data/images/bg_mat/IMG_4985.png",
    "avatarPng1": None,
    "garmentPng1": None,
    "garmentJson1": None,
    "category1": None,
    "avatarPng2": None,
    "garmentPng2": None,
    "garmentJson2": None,
    "category2": None
    }

    ao = await it.get_item_info(int(iid_ao))
    quan = await it.get_item_info(int(iid_quan))
    # khi user gui request den thi cac query parameter da co san trong databases va storage
    if ao == None and quan !=None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item shirt not found")
    if quan == None and ao !=None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item pant not found")
    if ao == None and quan == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item shirt and pant not found")
    category_ao = ao["category"]
    category_quan = quan["category"]
    
    # data["avatarPng1"] = "/home/edso/Documents/nguyen/libigl/tutorial/data/images/bg_mat/IMG_4988.png"
    # data["garmentPng1"] = "/home/edso/Documents/nguyen/libigl/tutorial/data/images/bg_mat/IMG_4988-1.png"
    # data["garmentJson1"] = "/home/edso/Documents/nguyen/libigl/tutorial/data/images/bg_mat/IMG_4988-1.json"
    # data["category1"] = "long_sleeve_top"
    # data["avatarPng2"] = "/home/edso/Documents/nguyen/libigl/tutorial/data/images/bg_mat/IMG_4988.png"
    # data["garmentPng2"] = "/home/edso/Documents/nguyen/libigl/tutorial/data/images/bg_mat/IMG_4988-1.png"
    # data["garmentJson2"] = "/home/edso/Documents/nguyen/libigl/tutorial/data/images/bg_mat/IMG_4988-1.json"
    # data["category2"] = "long_sleeve_top"
    
    # response = client.send(GetValues(data))
    # result = response.content
    # return result
    
    if category_ao == "dress":
        data["avatarPng1"] = ao["avatar"]
        data["garmentPng1"] = ao["garment"]
        data["garmentJson1"] = ao["garmentJson"]
        data["category1"] = category_ao
        data["avatarPng2"] = ao["avatar"]
        data["garmentPng2"] = ao["garment"]
        data["garmentJson2"] = ao["garmentJson"]
        data["category2"] = category_ao
        
        response = await client.send(GetValues(data=data))
        result = response.content
        return result
    
    elif category_ao != "dress":
        data["avatarPng1"] = ao["avarta"]
        data["garmentPng1"] = ao["garment"]
        data["garmentJson1"] = ao["garmentJson"]
        data["category1"] = category_ao
        data["avatarPng2"] = quan["avatar"]
        data["garmentPng2"] = quan["garment"]
        data["garmentJson2"] = quan["garmentJson"]
        data["category2"] = category_quan

        response = await client.send(GetValues(data=data))
        result = response.content
        return result

    if category_ao == "dress":
        url = "http://192.168.50.69:5849/{}/{}/{}/{}/{}/{}".format(int(iid_ao),category_ao,int(iid_ao),category_ao,4985,in_or_out)
        try:
            responses = requests.get(url=url, timeout=8)
            result = responses.content
            image = base64.b64decode(result)
            with open(filename, "wb") as f:
                f.write(image)
            return FileResponse("static/public/anh-tach-nen/image.png")
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)

    else:
        url = "http://192.168.50.69:5849/{}/{}/{}/{}/{}/{}".format(int(iid_quan),category_quan,int(iid_ao),category_ao,4985,in_or_out)
        try:
            responses = requests.get(url=url, timeout=8)
            result = responses.content
            image = base64.b64decode(result)
            with open(filename,"wb") as f:
                f.write(image)
            return FileResponse("static/public/anh-tach-nen/image.png")
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)

@router.get("/tryon_stateless/")
async def api_get_result_main(in_or_out: Optional[str] = "False", iid_ao: Optional[str] = "5010", iid_quan: Optional[str] = "4990"):

    # iid_ao = iid_ao.encode("windows-1252").decode("utf-8")
    # iid_quan = iid_quan.encode("windows-1252").decode("utf-8")
    # in_or_out = in_or_out.encode("windows-1252").decode("utf-8")

    ao = it.get_item_info(int(iid_ao))
    quan = it.get_item_info(int(iid_quan))
    category_ao = ao["category"]
    category_quan = quan["category"]

    if int(iid_ao) in dress_dict:
        url = "http://192.168.50.69:5849/{}/{}/{}/{}/{}".format(int(iid_ao),category_ao,int(iid_ao),category_ao,4985)
        response = requests.get(url=url, timeout=10)
        result = response.content
        image = base64.b64decode(result)
        with open(filename, 'wb') as f:
            f.write(image)
        return FileResponse("static/public/anh-tach-nen/image.png")
       
    
    else:
        url = "http://192.168.50.69:5849/{}/{}/{}/{}/{}".format(int(iid_quan),category_quan,int(iid_ao),category_ao,4985)
        response = requests.get(url=url, timeout=10)
        result = response.content
        image = base64.b64decode(result)
        with open(filename,"wb") as f:
            f.write(image)
        return FileResponse("static/public/anh-tach-nen/image.png")


    
    