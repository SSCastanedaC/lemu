import asyncio
import json
import threading

from kafka import KafkaConsumer
from pymongo import MongoClient

from settings import KAFKA_TOPIC, KAFKA_SERVER, TIMER_SAVER, MONGO_URL, MONGO_DB, MONGO_COLLECTION, KAFKA_PARTITIONS

client = MongoClient(MONGO_URL)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

ip_addresses = []


def read_messages(thread: int) -> None:
    """Reads messages from KafkaProducer and processes its content

    Parameters:
    - thread (int): Number of the thread as identifier

    Return:
    - None

    """
    print("Reader listening in thread:", thread)
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_SERVER,
        group_id = "KAFKA_GROUP"
    )
    for stream in consumer:
        message = json.loads(stream.value)
        ip_address = message["device_ip"]
        print(".", end="", flush=True)
        # Uncomment the next line to see which thread reads the message
        # print(thread, ip_address)
        ip_addresses.append({"ip_address": ip_address})


async def save_ip_addresses() -> None:
    """
    Saves elements from list into MongoDB collection

    Parameters:
    - None

    Return:
    - None
    """
    print("Saver listening...")
    while True:
        if ip_addresses:
            collection.insert_many(ip_addresses)
        print("Saving {} elements".format(len(ip_addresses)))
        ip_addresses.clear()
        await asyncio.sleep(TIMER_SAVER)


async def create_thread(number_threads: int) -> None:
    """
    Creates threads for Kafka Consumer to numberavoid blocking async tasks running in background

    Parameters:
    - number_threads (int): Numbers of threads to be created

    Return:
    - None
    """
    for i in range(number_threads):
        consumer_thread = threading.Thread(target=read_messages, args=(i,))
        consumer_thread.daemon = True
        consumer_thread.start()


async def main():
    """
    Runs the main coroutine
    """
    save_ip = asyncio.create_task(save_ip_addresses())
    asyncio.create_task(create_thread(KAFKA_PARTITIONS))
    await save_ip

asyncio.run(main())
