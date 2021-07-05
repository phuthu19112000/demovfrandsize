import mysql.connector

mydb = mysql.connector.connect(
  host="13.212.196.24",
  user="hieu",
  password="Hieu@1997",
  database="magento2"
)

mycursor = mydb.cursor()

# mycursor.execute("select * from eav_attribute_option_value")
# print(mycursor.column_names)
# for i in mycursor:
#     print(i)