class Fit_size:

    def __init__(self,user_measurement : dict ,item_info : dict , reference = "") -> None:
        
        self.user_measure = user_measurement
        self.item_info = item_info
        self.reference = reference
        self.category = self.item_info["category"]
        # Neu lam theo dua vao size chart co the danh trong so
        # cho tung loai vong khac nhau cho truong hop so do nam giua
        # 2 size

        if self.user_measure["sex"] == "Female":
            
            self.uc_bust = self.user_measure["bust_c"]
            self.uc_hip = self.user_measure["hip_c"]
            self.uc_waist = self.user_measure["waist_c"]
            self.uheight_shoulder = self.user_measure["height_shoulder"]
            self.uheight_hip = self.user_measure["height_hip"]
            self.inside_leg = self.user_measure["inside_leg"]

        if self.user_measure["sex"] == "Male":
            
            self.uc_chest = self.user_measure["chest_c"]
            self.uc_waist = self.user_measure["waist_c"]
            self.uc_hip = self.user_measure["hip_c"]
            self.uheight_shoulder = self.user_measure["height_shoulder"]
            self.uheight_hip = self.user_measure["height_hip"]
            self.inside_leg = self.user_measure["inside_leg"]
    
    def fit_size_female(self) -> dict:

        if self.category == "Top":

            if self.item_info["item"] == "Top" or self.item_info["item"] == "T-shirt":

                diff_length = self.uheight_shoulder - self.uheight_hip
                score = {}
                
                for key,value in self.item_info["attributes"].items():
                    key = key
                    val = 0
                    score.update({key:val})
                    chest_score = value["item_width_bust"] * 2 - self.uc_bust
                    length_top_score = value["item_length"] - diff_length
                    
                    if 0 <= chest_score <= 2:
                        score[key] += 1
                    if -1.5 <= length_top_score <= 1.5:
                        score[key] += 1
                
                # sort dict score
                score = {k:v for k,v in sorted(score.items(),key= lambda item : item[1])}
                score.update({"category": "Top", "item": "T-shirt"})
                return score

            if self.item_info["item"] == "Blouses":


                diff_length = self.uheight_shoulder - self.uheight_hip
                score = {}

                for key,value in self.item_info["attributes"].items():
                    key = key
                    val = 0
                    score.update({key:val})
                    chest_score = value["item_width_bust"] * 2 - self.uc_bust
                    length_top_score = value["item_length"] - diff_length
                    hip_score = value["item_width_hip"] * 2 - self.uc_hip

                    if 0 <= chest_score <= 2:
                        score[key] += 1
                    if 0 <= hip_score <= 4:
                        score[key] += 1
                    if -2 <= length_top_score <= 2:
                        score[key] += 1
                
                score = {k:v for k,v in sorted(score.items(),key= lambda item : item[1])}
                score.update({"category": "Top", "item": "Blouses"})
                return score

            if self.item_info["item"] == "Jacket" or self.item_info["item"] == "Blazers":
                
                diff_length = self.uheight_shoulder - self.uheight_hip
                score = {}

                for key,value in self.item_info["attributes"].items():
                    key = key
                    val = 0
                    score.update({key:val})
                    chest_score = value["item_width_bust"] * 2 - self.uc_bust
                    length_top_score = value["item_length"] - diff_length
                    
                    if 1.5 <= chest_score <= 4:
                        score[key] += 1
                    if -2 <= length_top_score <= 2:
                        score[key] += 1
                
                score = {k:v for k,v in sorted(score.items(),key= lambda item : item[1])}
                if self.item_info["item"] == "Jacket":
                    score.update({"category":"Top","item":"Jacket"})
                elif self.item_info["item"] == "Blazers":
                    score.update({"category":"Top","item":"Blazers"})
                return score
        
        if self.category == "Bottom":
            result = {}

            if self.item_info["item"] == "Short":
                score = {}

                for key,value in self.item_info["attributes"].items():
                    key = key
                    val = 0
                    score.update({key:val})
                    waist_score = value["item_width_waist"] * 2 - self.uc_waist
                    hip_score = value["item_width_hip"] * 2 - self.uc_hip

                    if 1 <= waist_score <= 2.5:
                        score[key] += 1
                    if 1 <= hip_score <= 2.5:
                        score[key] += 1
                
                score = {k:v for k,v in sorted(score.items(),key= lambda item : item[1])}
                score.update({"category":"Bottom","item":"Short"})
                return score

            if self.item_info["item"] == "Cropped pant":
                score = {}

                for key,value in self.item_info["attributes"].items():
                    key = key
                    val = 0
                    score.update({key:val})
                    waist_score = value["item_width_waist"] * 2 - self.uc_waist
                    hip_score = value["item_width_hip"] * 2 - self.uc_hip
                    inside_leg_score = self.inside_leg - value["item_inside_leg"]

                    if 1 <= waist_score <= 2.5:
                        score[key] += 1
                    if 1.5 <= hip_score <= 3:
                        score[key] += 1
                    if 3 <= inside_leg_score <= 6:
                        score[key] += 1
                
                score = {k:v for k,v in sorted(score.items(),key= lambda item : item[1])}
                score.update({"category":"Bottom","item":"Cropped pant"})
                return score

            if self.item_info["item"] == "Legging":
                score = {}

                for key,value in self.item_info["attributes"].items():
                    key = key
                    val = 0
                    score.update({key:val})
                    waist_score = value["item_width_waist"] * 2 - self.uc_waist
                    hip_score = value["item_widh_hip"] * 2 - self.uc_hip
                    inside_leg_score = self.inside_leg - value["item_inside_leg"]

                    if 0 <= waist_score <= 1:
                        score[key] += 1
                    if 0 <= hip_score <= 1:
                        score[key] += 1
                    if -1 <= inside_leg_score <= 1:
                        score[key] += 1
                
                score = {k:v for k,v in sorted(score.items(),key= lambda item : item[1])}
                score.update({"category":"Bottom","item":"Legging"})
                return score

            if self.item_info["item"] == "Jeans" or self.item_info["item"] == "Pants":
                score = {}

                for key,value in self.item_info["attributes"].items():
                    key = key
                    val = 0
                    score.update({key:val})
                    waist_score = value["item_width_waist"] * 2 - self.uc_waist
                    hip_score = value["item_width_hip"] * 2 - self.uc_hip
                    inside_leg_score = self.inside_leg - value["item_inside_leg"]

                    if 1 <= waist_score <= 2.5:
                        score[key] += 1
                    if 1 <= hip_score <= 3:
                        score[key] += 1
                    if -1.5 <= inside_leg_score <= 1.5:
                        score[key] += 1
                
                score = {k:v for k,v in sorted(score.items(),key= lambda item: item[1])}
                if self.item_info["item"] == "Jeans":
                    score.update({"category":"Bottom","item":"Jeans"})
                if self.item_info["item"] == "Pants":
                    score.update({"category":"Bottom","item":"Pants"})
                return score      

        if self.category == "Dress":

            if self.item_info["item"] == "Mini" or self.item_info["item"] == "Midi" \
                or self.item_info["item"] == "Maxi":

                score = {}
                for key,value in self.item_info["attributes"].items():
                    key = key
                    val = 0
                    score.update({key:val})

                    bust_score = value["item_width_bust"] * 2 - self.uc_bust
                    waist_score = value["item_width_waist"] * 2 - self.uc_waist
                    hip_score = value["item_width_hip"] * 2 - self.uc_hip

                    if 1 <= bust_score <= 3:
                        score[key] += 1
                    if 1 <= waist_score <= 5:
                        score[key] += 1
                    if hip_score > 0:
                        score[key] += 1

                score = {k:v for k,v in sorted(score.items(),key= lambda item : item[1])}
                if self.item_info["item"] == "Mini":
                    score.update({"category":"Dress","item":"Mini"})
                if self.item_info["item"] == "Midi":
                    score.update({"category":"Dress", "item":"Midi"})
                if self.item_info["item"] == "Maxi":
                    score.update({"category": "Dress", "item":"Maxi"})
                return score
        
        if self.category == "Skirt":

            if self.item_info["item"] == "Mini" or self.item_info["item"] == "Midi"\
                or self.item_info["item"] == "Maxi":

                score = {}
                for key,value in self.item_info["attributes"].items():
                    key = key
                    val = 0
                    score.update({key:val})
                    waist_score = value["item_width_waist"] - self.uc_waist
                    hip_score = value["item_width_hip"] - self.uc_hip

                    if 1 <= waist_score <= 3:
                        score[key]+=1
                    if hip_score > 0:
                        score[key]+=1
                score = {k:v for k,v in sorted(score.items(),key= lambda item : item[1])}
                if self.item_info["item"] == "Mini":
                    score.update({"category":"Skirt","item":"Mini"})
                if self.item_info["item"] == "Midi":
                    score.update({"category":"Skirt", "item":"Midi"})
                if self.item_info["item"] == "Maxi":
                    score.update({"category": "Skirt", "item":"Maxi"})
                return score

        if self.category == "Accessories":
            result = {}

            if self.item_info["item"] == "Shoes":
                pass

    def fit_size_male(self) -> dict:

        if self.category == "Shirt":

            if self.item_info["item"] == "Formal":
                pass
            if self.item_info["item"] == "Casual":
                pass
            if self.item_info["item"] == "Jacket" or self.item_info["item"] == "Blazers":
                
                diff_length = self.uheight_shoulder - self.uheight_hip
                score = {}

                for key,value in self.item_info["attributes"].items():
                    key = key
                    val = 0
                    score.update({key:val})
                    chest_score = value["item_width_bust"] * 2 - self.uc_chest
                    length_top_score = value["item_length"] - diff_length
                    
                    if 1.5 <= chest_score <= 4:
                        score[key] += 1
                    if -2 <= length_top_score <= 2:
                        score[key] += 1
                
                score = {k:v for k,v in sorted(score.items(),key= lambda item : item[1])}
                if self.item_info["item"] == "Jacket":
                    score.update({"category":"Shirt","item":"Jacket"})
                elif self.item_info["item"] == "Blazers":
                    score.update({"category":"Shirt","item":"Blazers"})
                    
                return score
        
        if self.category == "Pants":

            if self.item_info["item"] == "Short":
                score = {}

                for key,value in self.item_info["attributes"].items():
                    key = key
                    val = 0
                    score.update({key:val})
                    waist_score = value["item_width_waist"] * 2 - self.uc_waist
                    hip_score = value["item_width_hip"] * 2 - self.uc_hip
                    
                    if 1 <= waist_score <= 2.5:
                        score[key] += 1
                    if 1 <= hip_score <= 2.5:
                        score[key] += 1
                
                score = {k:v for k,v in sorted(score.items(),key= lambda item : item[1])}
                score.update({"category":"Pants","item":"Short"})
                return score

            if self.item_info["item"] == "Jeans":
                score = {}

                for key,value in self.item_info["attributes"].items():
                    key = key
                    val = 0
                    score.update({key:val})
                    waist_score = value["item_width_waist"] * 2 - self.uc_waist
                    hip_score = value["item_width_hip"] * 2 - self.uc_hip
                    inside_leg_score = self.inside_leg - value["item_inside_leg"]

                    if 1 <= waist_score <= 2.5:
                        score[key] += 1
                    if 1 <= hip_score <= 3:
                        score[key] += 1
                    if -1.5 <= inside_leg_score <= 1.5:
                        score[key] += 1
                
                score = {k:v for k,v in sorted(score.items(),key= lambda item: item[1])}
                if self.item_info["item"] == "Jeans":
                    score.update({"category":"Pants","item":"Jeans"})
                return score

