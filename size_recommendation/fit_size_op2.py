from _typeshed import SupportsDivMod
from time import sleep
from pydantic.errors import NoneIsAllowedError, NotNoneError
from database.db import UserDB

col = UserDB()

def cm(inches):
    return inches*2.54

# let uksizes = new Map();
# uksizes.set(4,"XXS");
# uksizes.set(6,"XS")
# uksizes.set(8,"S");
# uksizes.set(10,"M");
# uksizes.set(12,"L");
# uksizes.set(14,"XL");
# uksizes.set(16,"XXL");
# uksizes.set(18,"XXL");

# FEMALE
# Skirt mini,midi,maxi
skirtSizeChartZara=[
    {"size":"XXS", "waist": 58, "hip": 85.5},
    {"size":"XS", "waist": 62, "hip": 90},
    {"size":"S", "waist": 66, "hip": 94},
    {"size":"M", "waist": 70,"hip": 98},
    {"size":"L", "waist": 76,"hip": 104},
    {"size":"XL", "waist": 82,"hip": 110}
]
# Dress mini,midi,maxi,cocktail,sun,evening 
dressSizeChartZara = [
    {"size":"XXS", "bust": 80, "waist": 58, "hip": 85.5},
    {"size":"XS", "bust": 82, "waist": 62, "hip": 90},
    {"size":"S", "bust": 86.5, "waist": 66, "hip": 94},
    {"size":"M", "bust": 90, "waist": 70, "hip": 98},
    {"size":"L", "bust": 96, "waist": 76, "hip": 104},
    {"size":"XL", "bust": 102, "waist": 82, "hip": 110}
]

blousesSizeChartZara=[
    {"size":"XXS", "bust": 80, "waist": 58, "hip": 85.5},
    {"size":"XS", "bust": 82, "waist": 62, "hip": 90},
    {"size":"S", "bust": 86.5, "waist": 66, "hip": 94},
    {"size":"M", "bust": 90, "waist": 70, "hip": 98},
    {"size":"L", "bust": 96, "waist": 76, "hip": 104},
    {"size":"XL", "bust":102, "waist":82, "hip": 110}
]
# Blazers,Kimono,Vest,Windbreaker,Bomber
jacketsSizeChartZara = [
    {"size":"XXS", "bust": 80, "waist": 58, "hip": 85.5},
    {"size":"XS", "bust": 82, "waist": 62, "hip": 90},
    {"size":"S", "bust": 86.5, "waist": 66, "hip": 94},
    {"size":"M", "bust": 90, "waist": 70, "hip": 98},
    {"size":"L", "bust": 96, "waist": 76, "hip": 104},
    {"size":"XL", "bust":102, "waist":82, "hip": 110}
]
# jeans, pants, short
pantsSizeChart=[
    {"size":"XXS", "waist": 58, "hip": 85.5},
    {"size":"XS", "waist": 62, "hip": 90},
    {"size":"S", "waist": 66, "hip": 94},
    {"size":"M", "waist": 70,"hip": 98},
    {"size":"L", "waist": 76,"hip": 104},
    {"size":"XL", "waist": 82,"hip": 110}
]

tshirtSizeChartZara=[
    {"size":"XXS", "bust": 80, "waist": 58, "hip": 85.5},
    {"size":"XS", "bust": 82, "waist": 62, "hip": 90},
    {"size":"S", "bust": 86.5, "waist": 66, "hip": 94},
    {"size":"M", "bust": 90, "waist": 70, "hip": 98},
    {"size":"L", "bust": 96, "waist": 76, "hip": 104},
    {"size":"XL", "bust":102, "waist":82, "hip": 110}
]


class Fit_size:
    
    def __init__(self, uid: str, cat_item: str) -> None:
        self.uid = uid
        self.cat_item = cat_item
        
    def get_info_uid(self):
        #print(self.uid)
        result = col.get_user_info(self.uid)
        if result:
            return result
        else:
            return None
    
    def fit_size_female(self,info_user):

        if self.cat_item == "skirt" or self.cat_item == "pants":
            
            if info_user["waist"] <= 53 or info_user["hip"] <= 80:
                return None
            if info_user["waist"] >= 86 or info_user["hip"] >= 116:
                return None
            
            mindiffsum = 1000
            minsize = skirtSizeChartZara[0]["size"]
            for i in range(len(skirtSizeChartZara)):
                diff1 = 0
                diff2 = 0
                if info_user["waist"]:
                    diff1 = abs(skirtSizeChartZara[i]["waist"] - info_user["waist"])
                if info_user["hip"]:
                    diff2 = abs(skirtSizeChartZara[i]["hip"] - info_user["hip"])
                sumdiff = diff1 + diff2
                if sumdiff <= mindiffsum:
                    mindiffsum = sumdiff
                    minsize = skirtSizeChartZara[i]["size"]
            return minsize
        
        if self.cat_item == "dress":

            if info_user["bust"] <= 75 or info_user["waist"] <=54 or info_user["hip"] <= 80:
                return None
            if info_user["bust"] >= 106 or info_user["waist"] >=85 or info_user["hip"] >= 114:
                return None

            mindiffsum = 1000
            minsize = dressSizeChartZara[0]["size"]
            for i in range(len(dressSizeChartZara)):
                diff1 = 0
                diff2 = 0
                diff3 = 0
                if info_user["bust"]:
                    diff1 = abs(dressSizeChartZara[i]["bust"] - info_user["bust"])
                if info_user["waist"]:
                    diff2 = abs(dressSizeChartZara[i]["waist"] - info_user["waist"])
                if info_user["hip"]:
                    diff3 = abs(dressSizeChartZara[i]["hip"] - info_user["hip"])
                sumdiff = diff1 + diff2 + diff3
                if sumdiff <= mindiffsum:
                    mindiffsum = sumdiff
                    minsize = skirtSizeChartZara[i]["size"]
            return minsize
        
        if self.cat_item == "jacket":

            if info_user["bust"] <= 75 or info_user["waist"] <= 54 or info_user["hip"] <= 80:
                return None
            if info_user["bust"] >= 106 or info_user["waist"] >=85 or info_user["hip"] >= 114:
                return None
            
            mindiffsum = 1000
            minsize = jacketsSizeChartZara[0]["size"]
            for i in range(len(jacketsSizeChartZara)):
                diff1 = 0
                diff2 = 0
                diff3 = 0
                if info_user["bust"]:
                    diff1 = abs(jacketsSizeChartZara[i]["bust"] - info_user["bust"])
                if info_user["waist"]:
                    diff2 = abs(jacketsSizeChartZara[i]["waist"] - info_user["waist"])
                if info_user["hip"]:
                    diff3 = abs(jacketsSizeChartZara[i]["hip"] - info_user["hip"])
                sumdiff = diff1 + diff2 + diff3
                if sumdiff <= mindiffsum:
                    mindiffsum = sumdiff
                    minsize = jacketsSizeChartZara[i]["size"]
            return minsize
        
        if self.cat_item == "tshirt" or self.cat_item == "blouses":
            
            if info_user["bust"] <= 75 or info_user["waist"] <= 54 or info_user["hip"] <= 80:
                return None
            if info_user["bust"] >= 106 or info_user["waist"] >=85 or info_user["hip"] >= 114:
                return None

            mindiffsum = 1000
            minsize = tshirtSizeChartZara[0]["size"]
            for i in range(len(tshirtSizeChartZara)):
                diff1 = 0
                diff2 = 0
                diff3 = 0
                if info_user["bust"]:
                    diff1 = abs(tshirtSizeChartZara[i]["bust"] - info_user["bust"])
                if info_user["waist"]:
                    diff2 = abs(tshirtSizeChartZara[i]["waist"] - info_user["waist"])
                if info_user["hip"]:
                    diff3 = abs(tshirtSizeChartZara[i]["hip"] - info_user["hip"])
                sumdiff = diff1 + diff2 + diff3
                if sumdiff <= mindiffsum:
                    mindiffsum = sumdiff
                    minsize = tshirtSizeChartZara[i]["size"]
            return minsize 
    
    # đang pending 
    def fit_size_male(self,info_user):
        if self.cat_item == "Blouses":
            minidiffsum = 1000
            minsize = tshirtSizeChartZara[0]["size"]
            for i in range(len(tshirtSizeChartZara)):
                diff1 = 0
                diff2 = 0
                diff3 = 0
                if info_user["bust"]:
                    diff1 = abs(tshirtSizeChartZara[i]["bust"] - info_user["bust"])
                if info_user["waist"]:
                    diff2 = abs(tshirtSizeChartZara[i]["waist"] - info_user["waist"])
                if info_user["hip"]:
                    diff3 = abs(tshirtSizeChartZara[i]["hip"] - info_user["hip"])
                sumdiff = diff1 + diff2 + diff3
                if sumdiff <= minidiffsum:
                    minidiffsum = sumdiff
                    minsize = tshirtSizeChartZara[i]["size"]
            return minsize
        
    
