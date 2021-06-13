from pydantic.types import Json
from pymongo import MongoClient, message
from bson.objectid import ObjectId
from pydantic import BaseModel
from database.utils import norm_dict

URL = "mongodb+srv://hieule:0982298387@cluster0.qbwn8.gcp.mongodb.net"
NAME_DB = "ecommerce"

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(self):
        yield self.validate
    
    @classmethod
    def validate(self,v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)
    
    @classmethod
    def __modify_schema__(self,field_schema):
        field_schema.update(type="string")

class Singleton(type):
    __instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instance:
            cls.__instance[cls] = super(Singleton, cls).__call__(*args,**kwargs)
        return cls.__instance[cls]

class UserDB():

    __metaclass__ = Singleton

    def __init__(self, url = URL, db_name = NAME_DB ):
        self.database = MongoClient(url)[db_name]
        self.collection = self.database["users"]
    

    async def add_user(self, data: dict):
        user = self.collection.find_one({"userId": data["userId"]})
        if user:
            return None
        new_user = self.collection.insert_one(data)
        new_user = self.collection.find_one({"_id": new_user.inserted_id})
        return norm_dict(new_user)
    
    async def get_user_info(self, uid:str) -> dict:
        user = self.collection.find_one({"userId":uid})
        if user:
            return norm_dict(user)
        return None
    
    async def update_user(self, uid:str, data:dict):
        user = self.collection.find_one({"userId":uid})
        if user:
            is_update = self.collection.update_one(
                {"_id":user["_id"]}, {"$ser":data}
            )
            if is_update:
                return True
            else:
                return False
        return False
    
    async def del_user(self, uid:str):
        user = self.collection.find_one({"userId":uid})
        if user:
            self.collection.delete_one({"_id":user["_id"]})
            return True
        return False


class ItemDB():

    __metaclass__ = Singleton

    def __init__(self, url = URL, db_name = NAME_DB):
        self.database = MongoClient(url)[db_name]
        self.collection = self.database["items"]

    async def add_item(self,data:dict):
        item = self.collection.find_one({"itemId":data["itemId"]})
        if item:
            return None
        new_item = self.collection.insert_one(data)
        new_item = self.collection.find_one({"_id": new_item.inserted_id})
        return norm_dict(new_item)

    async def get_item_info(self, iid: str) -> dict:
        item = self.collection.find_one({"itemId": iid})
        if item:
            return norm_dict(item)
        return None
    
    async def update_item(self, iid: str, data: dict):
        item = self.collection.find_one({"itenId": iid})
        if item:
            is_update = self.collection.update_one(
                {"_id": item["_id"]}, {"$set": data}
            )
            if is_update:
                return True
            else:
                return False
        return False

    async def del_item(self, iid: str):
        item = self.collection.find_one({"itemId": iid})
        if item:
            self.collection.delete_one({"_id":item["_id"]})
            return True
        return False 


class UserSchema(BaseModel):
    userId: str
    sex: str
    
class ItemSchema(BaseModel):
    itemId: str
    name_image: str
    category: str
    path_base: str
    
    allow: str


