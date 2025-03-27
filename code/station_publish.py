from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from pymongo import MongoClient
import time
import json
import random

# AWS IoT Configuration
client = AWSIoTMQTTClient("station_001")
client.configureEndpoint("a222sb1v55uohs-ats.iot.us-east-1.amazonaws.com", 8883)
client.configureCredentials(
    "AmazonRootCA1.pem",
    "5151b322299156c1fdd06077d69008781ad3ad2da68eaf73f781b54c1ff95c9c-private.pem.key",
    "5151b322299156c1fdd06077d69008781ad3ad2da68eaf73f781b54c1ff95c9c-certificate.pem.crt",
)

client.configureOfflinePublishQueueing(-1)  # Infinite queue
client.configureDrainingFrequency(2)  # Draining: 2 Hz
client.configureConnectDisconnectTimeout(10)  # 10 sec
client.configureMQTTOperationTimeout(5)  # 5 sec

# Connect to AWS IoT
client.connect()

# MongoDB Configuration (Assuming MongoDB is running on localhost)
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["sensor_data"]
collection = db["readings"]

# Publish Data
while True:
    payload = {
        "station_id": "station_001",
        "temperature": round(random.uniform(-50, 50), 2),
        "humidity": round(random.uniform(0, 100), 2),
        "co2": random.randint(300, 2000),
        "timestamp": time.time(),
    }

    # Publish to AWS IoT
    client.publish("iot/sensors", json.dumps(payload), 1)

    # Store in MongoDB
    collection.insert_one(payload)

    # Single print statement
    print(f"Published & Stored: {payload}")

    time.sleep(5)
