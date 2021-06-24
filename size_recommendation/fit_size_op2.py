from pydantic.errors import NotNoneError
from database.db import ItemDB

col = ItemDB()

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

skirtSizeChartZara=[
    {"size":"XXS", "waist": 58, "hip": 85.5},
    {"size":"XS", "waist": 62, "hip": 90},
    {"size":"S", "waist": 66, "hip": 94},
    {"size":"M", "waist": 70,"hip": 98},
    {"size":"L", "waist": 76,"hip": 104},
    {"size":"XL", "waist": 82,"hip": 110}
]

dressSizeChartZara = [
    {"size":"XXS", "bust": 80, "waist": 58, "hip": 85.5},
    {"size":"XS", "bust": 82, "waist": 62, "hip": 90},
    {"size":"S", "bust": 86.5, "waist": 66, "hip": 94},
    {"size":"M", "bust": 90, "waist": 70, "hip": 98},
    {"size":"L", "bust": 96, "waist": 76, "hip": 104},
    {"size":"XL", "bust": 102, "waist": 82, "hip": 110}
]

jacketsSizeChartZara = [
    {"size":"XXS", "bust": 80, "waist": 58, "hip": 85.5},
    {"size":"XS", "bust": 82, "waist": 62, "hip": 90},
    {"size":"S", "bust": 86.5, "waist": 66, "hip": 94},
    {"size":"M", "bust": 90, "waist": 70, "hip": 98},
    {"size":"L", "bust": 96, "waist": 76, "hip": 104},
    {"size":"XL", "bust":102, "waist":82, "hip": 110}
]

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

blousesSizeChartZara=[
    {"size":"XXS", "bust": 80, "waist": 58, "hip": 85.5},
    {"size":"XS", "bust": 82, "waist": 62, "hip": 90},
    {"size":"S", "bust": 86.5, "waist": 66, "hip": 94},
    {"size":"M", "bust": 90, "waist": 70, "hip": 98},
    {"size":"L", "bust": 96, "waist": 76, "hip": 104},
    {"size":"XL", "bust":102, "waist":82, "hip": 110}
]

class Fit_size:
    
    def __init__(self, uid: int, cat_item: str) -> None:
        self.uid = uid
        self.cat_item = cat_item
        
    async def get_info_uid(self):
        result = await col.get_item_info(self.uid)
        print(result)
        if result:
            return result
        else:
            return None
    
    def fit_size_female(self,info_user):

        
        if self.cat_item == "skirt" or self.cat_item == "pants":
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
        
