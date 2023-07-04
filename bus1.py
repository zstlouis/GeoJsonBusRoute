from pykafka import KafkaClient
import json
from datetime import datetime
import uuid
import time

# Read coordinates from geojson
input_file = open('./data/bus1.json')
json_array = json.load(input_file)
coordinates = json_array['features'][0]['geometry']['coordinates']


# generate uuid
def generate_uuid():
    return uuid.uuid4()


# Kafka Producer
client = KafkaClient(hosts="localhost:9092")
topic = client.topics['geodata_final']
producer = topic.get_sync_producer()

# construct message send it to kafka
data = {}
data['busline'] = '00001'


def generate_checkpoint(coordinates):
    i = 0
    while i < len(coordinates):
        data['key'] = data['busline'] + "_" + str(generate_uuid())
        data['timestamp'] = str(datetime.utcnow())
        data['latitude'] = coordinates[i][1]
        data['longitude'] = coordinates[i][0]
        message = json.dumps(data)
        print(message)
        producer.produce(message.encode('ascii'))
        time.sleep(1)

        # start again once last coordinate is reached
        if i == len(coordinates)-1:
            i = 0
        else:
            i+=1


generate_checkpoint(coordinates)

"""
client = KafkaClient(hosts="localhost:9092")

topic = client.topics['testBusdata']


producer = topic.get_sync_producer()


producer.produce("test".encode('ascii'))

"""

# testBusdata
