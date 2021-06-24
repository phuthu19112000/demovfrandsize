from kafka import KafkaConsumer, consumer
import json
from database.db import CityDB

col = CityDB()

consumer = KafkaConsumer(
    "hieuld.magento2.customer_address_entity",
    bootstrap_servers = "localhost:9092",
    auto_offset_reset = "earliest",
    enable_auto_commit=True,
    group_id = "consumer_VFR",
    request_time_out = 305000,
    reconnect_backoff_ms = 50,
    heartbeat_interval_ms = 3000,
    security_protocol = "PLAINTEXT"
)

async def sync_to_mongo(payload: dict) -> str:

    if payload["op"] == "r":
        data = payload["after"]
        result = await col.add_item(data)
        if result:
            msg = "Successfully SNAPSHOT records with id={} into MongoDB".format(data["id"])
            return msg
        elif result == None:
            msg = "Faild SNAPSHOT records with id={} into MongoDB".format(data["id"])
            return msg
    
    if payload["op"] == "u":
        data = payload["after"]
        ID = data["id"]
        result = await col.update_item(ID,data)
        if result:
            msg = "Successfully update records with id={} into MongoDB".format(data["id"])
            return msg
        else:
            msg = "Faild update records with id={} into MongoDB".format(data["id"])
            return msg
    
    if payload["op"] == "c":
        data = payload["after"]
        result = await col.add_item(data)
        if result:
            msg = "Successfully create records with id={} into MongoDB".format(data["id"])
            return msg
        elif result == None:
            msg = "Faild create records with id={} into MongoDB".format(data["id"])
            return msg

    if payload["op"] == "d":
        data = payload["before"]
        ID = data["id"]
        result = await col.del_item(ID)
        if result:
            msg = "Successfully delete records with id={} from MongoDB".format(data["id"])
            return msg
        else:
            msg = "Faild delete records with id={} from MongoDB".format(data["id"])
            return msg

for msg in consumer:
    if msg.value != None:
        msg = msg.value.decode("utf-8")
        msg = json.loads(msg)
        payload = msg["payload"]
        result = sync_to_mongo(payload=payload)
        print(result)
    elif msg.value == None:
        continue