from pydantic.errors import NotNoneError
from pydantic.types import Json
from pymongo import MongoClient, message
from bson.objectid import ObjectId
from pydantic import BaseModel, Field
from database.utils import norm_dict
from typing import Optional

#URL = "mongodb+srv://hieule:0982298387@cluster0.qbwn8.gcp.mongodb.net"
URL = "mongodb://118.70.181.146:2100"
NAME_DB = "magento2"

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
    

    def add_user(self, data: dict):
        user = self.collection.find_one({"id": data["userId"]})
        if user:
            return None
        new_user = self.collection.insert_one(data)
        new_user = self.collection.find_one({"_id": new_user.inserted_id})
        return norm_dict(new_user)
    
    def get_user_info(self, uid:str) -> dict:
        
        user = self.collection.find_one({"id":uid})
        if user:
            return norm_dict(user)
        return None
    
    def update_user(self, uid:str, data:dict):
        user = self.collection.find_one({"id":uid})
        if user:
            is_update = self.collection.update_one(
                {"_id":user["_id"]}, {"$set":data}
            )
            if is_update:
                return True
            else:
                return False
        return False
    
    def del_user(self, uid:str):
        user = self.collection.find_one({"id":uid})
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

    # async def get_item_info(self, iid: str) -> dict:
    #     item = self.collection.find_one({"itemId": iid})
    #     if item:
    #         return norm_dict(item)
    #     return None

    async def get_item_info(self, iid: int) -> dict:
        item = self.collection.find_one({"iid":iid})
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


class CityDB():

    __metaclass__ = Singleton

    def __init__(self, url = URL, db_name = NAME_DB):
        self.database = MongoClient(url)[db_name]
        self.collection = self.database["items"]

    def add_item(self,data:dict):
        item = self.collection.find_one({"entity_id":data["entity_id"]})
        if item:
            return None
        new_item = self.collection.insert_one(data)
        new_item = self.collection.find_one({"_id": new_item.inserted_id})
        return norm_dict(new_item)

    def get_item_info(self, iid: str) -> dict:
        item = self.collection.find_one({"entity_id": iid})
        if item:
            return norm_dict(item)
        return None
    
    def update_item(self, iid: str, data: dict):
        item = self.collection.find_one({"entity_id": iid})
        if item:
            is_update = self.collection.update_one(
                {"_id": item["_id"]}, {"$set": {"type_id":data["type_id"], "sku":data["sku"]}}
            )
            if is_update:
                return True
            else:
                return False
        return False

    def del_item(self, iid: str):
        item = self.collection.find_one({"entity_id": iid})
        if item:
            self.collection.delete_one({"_id":item["_id"]})
            return True
        return False 

class Att2value():
    __metaclass__ = Singleton

    def __init__(self, url = URL, db_name = NAME_DB):
        self.database = MongoClient(url)[db_name]
        self.collection = self.database["attribute_id2value"]

    def add_item(self,data:dict):
        item = self.collection.find_one({"attribute_id":data["attribute_id"]})
        if item:
            return None
        new_item = self.collection.insert_one(data)
        new_item = self.collection.find_one({"_id": new_item.inserted_id})
        return norm_dict(new_item)

    def get_item_info(self, iid: str) -> dict:
        item = self.collection.find_one({"attribute_id": iid})
        if item:
            return norm_dict(item)
        return None
    
    def update_item(self, iid: str, data: dict):
        item = self.collection.find_one({"attribute_id": iid})
        if item:
            is_update = self.collection.update_one(
                {"_id": item["_id"]}, {"$set": data}
            )
            if is_update:
                return True
            else:
                return False
        return False

    def del_item(self, iid: str):
        item = self.collection.find_one({"attribute_id": iid})
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

class ItemTryon(BaseModel):
    
    iid_ao: Optional[str] = "200"
    iid_quan: Optional[str] = "300"

