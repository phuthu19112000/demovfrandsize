import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

  
### Lap size chart cho quần áo nữ
# size_chart chung cho quan ao
chart_general_clothes = {"height": ["150-155","156-160","160-164","165-170"],
                        "weight": ["40-45","43-46","46-53","53-57"],
                        "bust": ["78-82","84-88","88-92","92-96"],
                        "waist": ["64-68","68-72","72-76","76-80"],
                        "hip": ["86-90","90-94","94-98","98-102"]}
df_female_gen = pd.DataFrame(chart_general_clothes, index =['S','M','L','XL'])
df_female_gen.to_csv ('/home/hieuld/FRS/Size_RS/size_charts/female/df_female_gen.csv', index = True, header=True)

# size chart cho dong quan ao Body,Heatech
chart_body_shirt = {"bust": ["80-84","84-88","88-92","92-96"],
                    "dai ao": [57.5,59.5,61.5,62.5],
                    "dai tay": [56,57,58,59]}
df_body_shirt = pd.DataFrame(chart_body_shirt, index= ["S","M","L","XL"])
df_body_shirt.to_csv("/home/hieuld/FRS/Size_RS/size_charts/female/df_body_shirt.csv", index= True, header= True)

chart_body_pant = {"waist": ["64-68","68-72","72-76","76-80"],
                   "hip": ["86-90","90-94","94-98","98-102"],
                   "dai quan": [86.5,88.5,90.5,91.5]}
df_body_pant = pd.DataFrame(chart_body_pant, index= ["S","M","L","XL"])
df_body_pant.to_csv("/home/hieuld/FRS/Size_RS/size_charts/female/df_body_pant.csv", index= True, header= True)

# size chart quan au
chart_quan_au = {"waist": ["64-68","68-72","72-76","76-80"],
                 "hip": ["86-90","90-94","94-98","98-102"],
                 "dai quan": [90.5,92.5,94.5,95.5]}
df_quan_au = pd.DataFrame(chart_quan_au, index=["S","M","L","XL"])
df_quan_au.to_csv("/home/hieuld/FRS/Size_RS/size_charts/female/df_quan_au.csv", index= True, header= True)

# size chart quan kaki
chart_quan_kaki = {"waist": ["60-64","64-68","68-72","72-76","76-80"],
                   "hip": ["82-86","86-90","90-94","94-98","98-102"],
                   "dai giang": [73.5,74,75.7,75.4,76.1]}
df_quan_kaki = pd.DataFrame(chart_quan_kaki, index= [26,27,28,29,30])
df_quan_kaki.to_csv("/home/hieuld/FRS/Size_RS/size_charts/female/df_quan_kaki.csv", index= True, header=True)

# Size chart ao khoac
chart_ao_khoac = {"rong vai": ["34-36","36-38","38-40","40-42"],
                  "dai ao": [60.5,62.5,64.5,65.5],
                  "vong nguc": ["80-84","84-88","88-92","92-96"],
                  "dai tay": [59.5,60.5,61.5,62.5]}
df_ao_khoac = pd.DataFrame(chart_ao_khoac,index=["S","M","L","XL"])
df_ao_khoac.to_csv("/home/hieuld/FRS/Size_RS/size_charts/female/df_ao_khoac.csv", index= True, header= True)

# Size chart vay lien om
chart_vay_lien_om = {"height": ["150-155","156-160","160-164","165-170"],
                     "bust": ["80-84","84-88","88-92","92-96"],
                     "waist": ["64-68","68-72","72-76","76-80"],
                     "hip": ["86-90","90-94","94-98","98-102"],
                     "rong vai": ["34-36","36-38","38-40","40-42"],
                     "dai vay": [89,92,94,96]}
df_vay_lien_om = pd.DataFrame(chart_vay_lien_om, index= ["S","M","L","XL"])
df_vay_lien_om.to_csv("/home/hieuld/FRS/Size_RS/size_charts/female/df_vay_lien_om.csv", index= True, header= True)

# Size chart vay lien xuong
char_vay_lien_suong = {"height": ["150-155","156-160","160-164","165-170"],
                     "bust": ["80-84","84-88","88-92","92-96"],
                     "hip": ["86-90","90-94","94-98","98-102"],
                     "rong vai": ["34-36","36-38","38-40","40-42"],
                     "dai vay": [82,85,87,None]}
df_vay_lien_suong = pd.DataFrame(char_vay_lien_suong, index= ["S","M","L","XL"])
df_vay_lien_suong.to_csv("/home/hieuld/FRS/Size_RS/size_charts/female/df_vay_lien_suong.csv", index= True, header= True)



### Lap size chart cho quan ao nam
# Size chart chung cho quan ao
chart_general_clothes = {"height": ["165-167","168-170","170-173","173-176"],
                         "weight": ["55-60","60-65","66-70","70-76"],
                         "bust": ["86-90","90-94","94-98","98-102"],
                         "waist": ["68-72","72-76","76-80","80-84"],
                         "hip": ["88-92","92-96","96-100","100-104"]}
df_general_clothes = pd.DataFrame(chart_general_clothes)