from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pymongo import message
from database.db import UserSchema,UserDB
from routers.utils import ResponseModel, ErrorResponseModel

router = APIRouter()
user_col = UserDB()

#CREATE
@router.post("/users/")
async def api_add_user(data: UserSchema) -> dict:
    """
    Add user to db
    """
    data = jsonable_encoder(data)
    new_user = user_col.add_user(data)
    if new_user:
        message = "add success"
        code = 201
        return ResponseModel(new_user, code, message)
    return ErrorResponseModel("Faild", 404)

#READ
@router.get("/users/{uid}")
async def api_get_user_info(uid : str) -> dict:
    """
    Get user from db
    """
    user = user_col.get_user_info(uid)
    if user:
        message = "Success"
        code = 200
        return ResponseModel(user, code, message)
    return ErrorResponseModel("Faild", 404)

#UPDATE
@router.put("/users/{uid}")
async def api_update_user(uid: str, data: UserSchema) -> dict:
    """
    Update user in db
    """
    data = jsonable_encoder(data)
    is_update = user_col.update_user(uid,data)
    if is_update:
        message = "Update Success"
        code = 200
        return ResponseModel(is_update, code, message)
    return ErrorResponseModel("Faild", 404)

#DELETE
@router.delete("/users/{uid}")
async def api_del_user(uid: str) -> dict:
    """
    Delete user in db
    """
    is_del = user_col.del_user(uid)
    if is_del:
        message = "Delete Success"
        code = 200
        return ResponseModel(is_del, code, message)
    return ErrorResponseModel("Faild",404)


