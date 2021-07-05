import sys
sys.path.append("D:\demovfrandsize")
import requests
from kafka import KafkaConsumer, consumer
import json
from database.db import CityDB
# https://github.com/tjworks/kafka-mongodb-debezium-demo/blob/master/consumer.py
# https://medium.com/swlh/sync-mysql-to-postgresql-using-debezium-and-kafkaconnect-d6612489fd64
# curl -X DELETE http://localhost:8083/connectors/<connector-name>
# .\bin\windows\kafka-topics.bat --list --zookeeper localhost:2181 (list all topic in kafka broker)
# kafka-topics.sh --delete --zookeeper localhost:2181 --topic your_topic_name

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

def sync_to_mongo(payload: dict) -> str:
   
    if payload["op"] == "r":
        
        data = payload["after"]
        result = col.add_item(data)
        if result:
            msg = "Successfully SNAPSHOT records with id={} into MongoDB".format(data["entity_id"])
            return msg
        elif result == None:
            msg = "Faild SNAPSHOT records with id={} into MongoDB".format(data["entity_id"])
            return msg
    
    if payload["op"] == "u":
        data = payload["after"]
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
        result = col.add_item(data)
        if result:
            msg = "Successfully create records with id={} into MongoDB".format(data["entity_id"])
            return msg
        elif result == None:
            msg = "Faild create records with id={} into MongoDB".format(data["entity_id"])
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
        count += 1
        if count == 50:
            requests.get(url="http://118.70.181.146:2101/engine/reload")
            print(result)
            count = 0
    elif msg.value == None:
        continue
