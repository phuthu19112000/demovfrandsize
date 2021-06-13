from routers.utils import ErrorResponseModel, ResponseModel
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pymongo import message
from database.db import ItemSchema, ItemDB
from routers.utils import ResponseModel, ErrorResponseModel


router = APIRouter()
item_col = ItemDB()

#CREATE
@router.post("/items/")
async def api_add_item(data: ItemSchema) -> dict:
    """
    Add item to db
    """
    data = jsonable_encoder(data)
    new_item = item_col.add_item(data)
    if new_item:
        message = "add success"
        code = 201
        return ResponseModel(new_item, code, message)
    return ErrorResponseModel("Faild",404)

#READ
@router.get("items/{iid}")
async def api_get_item(iid: str) -> dict:
    """
    Get item from db
    """
    item = item_col.get_item_info(iid)
    if item:
        message = "Success"
        code = 200
        return ResponseModel(item,code,message)
    return ErrorResponseModel("Faild",404)

#UPDATE
@router.put("/items/{iid}")
async def api_update_item(iid: str, data: ItemSchema) -> dict:
    """
    Update item in db
    """
    data = jsonable_encoder(data)
    is_update = item_col.update_item(iid,data)
    if is_update:
        message = "update success"
        code = 200
        return ResponseModel(is_update,code,message)
    return ErrorResponseModel("Faild",404)

#DELETE
@router.delete("/items/{iid}")
async def api_delete_item(iid:str) -> dict:
    """
    Delete item in db
    """
    is_del = item_col.del_item(iid)
    if is_del:
        message = "Delete success"
        code = 200
        return ResponseModel(is_del, code, message)
    return ErrorResponseModel("Faild",404)

