import sys
sys.path.append("D:\demovfrandsize")
import requests
from kafka import KafkaConsumer, consumer
import json
from database.db import CityDB
from connect_mysql_magento.connect_mysql_magento import mydb

# https://github.com/tjworks/kafka-mongodb-debezium-demo/blob/master/consumer.py
# https://medium.com/swlh/sync-mysql-to-postgresql-using-debezium-and-kafkaconnect-d6612489fd64
# curl -X DELETE http://localhost:8083/connectors/<connector-name>
# .\bin\windows\kafka-topics.bat --list --zookeeper localhost:2181 (list all topic in kafka broker)
# kafka-topics.sh --delete --zookeeper localhost:2181 --topic your_topic_name
cursor1 = mydb.cursor(buffered=True)
cursor2 = mydb.cursor(buffered=True)
#cursor1.execute("select * from catalog_product_entity_media_gallery_value")
#cursor2.execute("select * from catalog_product_entity_media_gallery")

col = CityDB()

consumer = KafkaConsumer(
    "hieuld.magento2.catalog_product_entity",
    bootstrap_servers = "localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    auto_commit_interval_ms=5000,
    reconnect_backoff_ms = 50,
    heartbeat_interval_ms = 3000,
    security_protocol = "PLAINTEXT"
)

def drop_column(data):

    data.pop("attribute_set_id")
    data.pop("has_options")
    data.pop("required_options")
    data.pop("created_at")
    data.pop("updated_at")
    return data

def sync_to_mongo(payload: dict) -> str:
   
    if payload["op"] == "r":
        
        data = payload["after"]
        data = drop_column(data)
        entity_id = data["entity_id"]
        cursor1.execute("select value_id from catalog_product_entity_media_gallery_value where entity_id={}".format(entity_id))
        path_img = []
        for i in cursor1:
            value_id = i[0]
            cursor2.execute("select value from catalog_product_entity_media_gallery where value_id={}".format(value_id))
            for j in cursor2:
                image_path = j[0]
            path_img.append(image_path)
        data.update({"image path": path_img})
        result = col.add_item(data)
        if result:
            msg = "Successfully SNAPSHOT records with id={} into MongoDB".format(data["entity_id"])
            return msg
        elif result == None:
            msg = "Faild SNAPSHOT records with id={} into MongoDB".format(data["entity_id"])
            return msg
    
    if payload["op"] == "u":
        data = payload["after"]
        data = drop_column(data)

        ID = data["entity_id"]
        result = col.update_item(ID,data)
        if result:
            msg = "Successfully update records with id={} into MongoDB".format(data["entity_id"])
            return msg
        else:
            msg = "Faild update records with id={} into MongoDB".format(data["entity_id"])
            return msg
    
    if payload["op"] == "c":
        data = payload["after"]
        data = drop_column(data)
        entity_id = data["entity_id"]
        cursor1.execute("select value_id from catalog_product_entity_media_gallery_value where entity_id={}".format(entity_id))
        path_img = []
        for i in cursor1:
            value_id = i[0]
            cursor2.execute("select value from catalog_product_entity_media_gallery where value_id={}".format(value_id))
            for j in cursor2:
                image_path = j[0]
            path_img.append(image_path)
        data.update({"image path": path_img})
        result = col.add_item(data)
        if result:
            msg = "Successfully SNAPSHOT records with id={} into MongoDB".format(data["entity_id"])
            return msg
        elif result == None:
            msg = "Faild SNAPSHOT records with id={} into MongoDB".format(data["entity_id"])
            return msg

    if payload["op"] == "d":
        data = payload["before"]
        ID = data["entity_id"]
        result = col.del_item(ID)
        if result:
            msg = "Successfully delete records with id={} from MongoDB".format(data["entity_id"])
            return msg
        else:
            msg = "Faild delete records with id={} from MongoDB".format(data["entity_id"])
            return msg

#count = 0
for msg in consumer:
    if msg.value != None:
        msg = msg.value.decode("utf-8")
        msg = json.loads(msg)
        payload = msg["payload"]
        result = sync_to_mongo(payload=payload)
        print(result)
        # count += 1
        # if count == 50:
        #     requests.get(url="http://118.70.181.146:2101/engine/reload")
        #     print(result)
        #     count = 0
    elif msg.value == None:
        continue
