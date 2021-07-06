import mysql.connector

mydb = mysql.connector.connect(
  host="13.212.196.24",
  user="hieu",
  password="Hieu@1997",
  database="magento2"
)

mycursor = mydb.cursor()

mycursor.execute("select value from catalog_product_entity_media_gallery where value_id=104")

for i in mycursor:
  print(i[0])
# print(mycursor.value())