import sys
sys.path.append("D:\demovfrandsize")
import requests
from kafka import KafkaConsumer, consumer
import json
from database.db import Att2value
from connect_mysql_magento.connect_mysql_magento import mycursor

# https://github.com/tjworks/kafka-mongodb-debezium-demo/blob/master/consumer.py
# https://medium.com/swlh/sync-mysql-to-postgresql-using-debezium-and-kafkaconnect-d6612489fd64
# curl -X DELETE http://localhost:8083/connectors/<connector-name>
# .\bin\windows\kafka-topics.bat --list --zookeeper localhost:2181 (list all topic in kafka broker)
# kafka-topics.sh --delete --zookeeper localhost:2181 --topic your_topic_name

col = Att2value()

consumer = KafkaConsumer(
    "hieuld.magento2.eav_attribute_label",
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
        data.pop("attribute_label_id")
        data.pop("store_id")
        result = col.add_item(data)
        if result:
            return "Successfully"
        elif result == None:
            return "Faild"
        
    
    if payload["op"] == "u":
        data = payload["after"]
        data.pop("attribute_label_id")
        data.pop("store_id")
        ID = data["attribute_id"]
        result = col.update_item(ID,data)
        if result:
            return "Successfully"
        else:
            return "Faild"
       
    
    if payload["op"] == "c":
        data = payload["after"]
        data.pop("attribute_label_id")
        data.pop("store_id")
        result = col.add_item(data)
        if result:
            return "Successfully"
        elif result == None:
            return "Faild"

    if payload["op"] == "d":
        data = payload["before"]
        data.pop("attribute_label_id")
        data.pop("store_id")
        ID = data["attribute_id"]
        result = col.del_item(ID)
        if result:
            return "Successfully"
        else:
            return "Faild"

#count = 0
for msg in consumer:
    if msg.value != None:
        msg = msg.value.decode("utf-8")
        msg = json.loads(msg)
        payload = msg["payload"]
        result = sync_to_mongo(payload=payload)
        print(result)
    elif msg.value == None:
        continue

