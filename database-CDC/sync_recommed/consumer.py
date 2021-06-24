from kafka import KafkaConsumer, consumer
import json
from database.db import CityDB
# https://github.com/tjworks/kafka-mongodb-debezium-demo/blob/master/consumer.py
# https://medium.com/swlh/sync-mysql-to-postgresql-using-debezium-and-kafkaconnect-d6612489fd64
# curl -X DELETE http://localhost:8083/connectors/<connector-name>
# .\bin\windows\kafka-topics.bat --list --zookeeper localhost:2181 (list all topic in kafka broker)
# kafka-topics.sh --delete --zookeeper localhost:2181 --topic your_topic_name

# {
#     "name": "inventory-connector",
#     "config": {
#         "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
#         "tasks.max": 1,
#         "database.hostname": "postgres",
#         "database.port": 5432,
#         "database.user": "postgres",
#         "database.password": "postgres",
#         "database.dbname" : "postgres",
#         "database.server.name": "dbserver1",
#         "schema.include.list": "inventory",

#         "topic.creation.default.replication.factor": 3,
#         "topic.creation.default.partitions": 10,
#         "topic.creation.default.cleanup.policy": "compact",
#         "topic.creation.default.compression.type": "lz4"
#     }
# }


col = CityDB()

consumer = KafkaConsumer(
    "hieuld.magento2.customer_address_entity",
    bootstrap_servers = "localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    auto_commit_interval_ms=5000,
    group_id = 'consumer_recommender',
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
