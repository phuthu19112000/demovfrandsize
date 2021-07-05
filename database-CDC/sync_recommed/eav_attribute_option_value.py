import sys
from pymongo import results
sys.path.append("D:\demovfrandsize")
import requests
from kafka import KafkaConsumer, consumer
import json
from connect_mysql_magento.connect_mysql_magento import mycursor


# mycursor.execute("select attribute_id from eav_attribute_option where option_id=90")
# for i in mycursor:
#     print(type(i[0]))

consumer = KafkaConsumer(
    "hieuld.magento2.eav_attribute_option_value",
    bootstrap_servers = "localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    auto_commit_interval_ms=5000,
    reconnect_backoff_ms=50,
    heartbeat_interval_ms=3000,
    security_protocol="PLAINTEXT"
)

def sync_to_mongo(payload):
    pass

for msg in consumer:
    if msg.value != None:
        msg = msg.value.decode("utf-8")
        msg = json.loads(msg)
        payload = msg["payload"]
        result = sync_to_mongo(payload=payload)
    elif msg.value == None:
        continue

# Test code
consumer2 = KafkaConsumer(
    "hieuld.magento2.eav_attribute_option"
)