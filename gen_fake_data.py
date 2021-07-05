
# import random
# from pymongo import MongoClient

# URL = "mongodb://118.70.181.146:2100"
# NAME_DB = "fashion"
# database = MongoClient(URL)[NAME_DB]
# collection = database["items"]
# result = collection.find( {} )
# size = ["XXS","XS","S","M","L","XL"]
# category = ["skirt","pants","dress","jacket","tshirt","blouses"]
# for i in result:
#     # mesures["bust"] = random.uniform(70.0,120.0)
#     # mesures["hip"] = random.uniform(75.0,120.0)
#     # mesures["waist"] = random.uniform(50.0,90.0)
#     # index = random.randint(0, 5)
#     # cat = category[index]
#     # collection.update_one({"_id":i["_id"]},{"$set": {"size": size,"category" : cat}})
    
#     print(i)import re
import time
from pymongo import MongoClient
import base64

# with open("/home/hieuld/project_RS_VFR/demo_web_VFR/static/public/anh-tach-nen/image.png", "rb") as img_file:
#     my_string = base64.b64encode(img_file.read())

URL = "mongodb+srv://hieule:0982298387@cluster0.qbwn8.gcp.mongodb.net/?authSource=admin&replicaSet=atlas-u5m786-shard-0&readPreference=primary&ssl=true"
NAME_DB = "ecommerce"
database = MongoClient(URL)[NAME_DB]
collection = database["items"]

time_list = []

for i in range(20):

    start = time.time()
    result = collection.find_one( {} )["string base64"]
    diff = time.time() - start
    time_list.append(diff)
    print(diff)
print("Time avg to load: {}".format(sum(time_list)/len(time_list)))

