import argparse
import json
import random
import time
from datetime import datetime, timezone

from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaProducer

from settings import KAFKA_TOPIC, KAFKA_SERVER, TIMER_PRODUCER, KAFKA_PARTITIONS

TIMESTAMP_FORMATS = [
    '%Y-%m-%dT%H:%M:%S.%fZ',
    '%Y-%m-%dT%H:%M:%S.%f',
    '%Y-%m-%dT%H:%M:%S',
    'unix_millis',
    'unix_seconds',
]


def generate_timestamp():
    fmt = random.choice(TIMESTAMP_FORMATS)
    now = datetime.now(timezone.utc)
    if fmt == 'unix_millis':
        return str(int(now.timestamp() * 1000))
    elif fmt == 'unix_seconds':
        return str(int(now.timestamp()))
    else:
        return now.strftime(fmt)


def generate_device_ip():
    return '.'.join(str(random.randint(0, 255)) for _ in range(4))


def main():
    parser = argparse.ArgumentParser(description='Kafka Message Sender')
    parser.add_argument('--topic', default=KAFKA_TOPIC, help='Kafka topic to send messages to')
    parser.add_argument('--bootstrap_servers', default=KAFKA_SERVER, help='Kafka bootstrap servers')
    parser.add_argument('--num_devices', type=int, default=100, help='Number of devices to simulate')
    parser.add_argument('--pause_ms', type=int, default=TIMER_PRODUCER, help='Pause between messages in milliseconds')
    parser.add_argument('--num_messages', type=int, default=1000, help='Total number of messages to send')
    args = parser.parse_args()

    # Adds Kafka Client parameters to set the number of partitions 
    admin_client = KafkaAdminClient(bootstrap_servers=KAFKA_SERVER, client_id='test_admin')
    try:
        admin_client.delete_topics([KAFKA_TOPIC])
    except:  # noqa: E722
        pass
    topic_list = [NewTopic(name=KAFKA_TOPIC, num_partitions=KAFKA_PARTITIONS, replication_factor=1)]
    admin_client.create_topics(new_topics=topic_list, validate_only=False)

    producer = KafkaProducer(
        bootstrap_servers=args.bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    device_ips = [generate_device_ip() for _ in range(args.num_devices)]

    for i in range(args.num_messages):
        message = {
            'timestamp': generate_timestamp(),
            'device_ip': random.choice(device_ips),
            'error_code': random.randint(0, 10)
        }
        key_bytes = message["device_ip"].encode('utf-8')
        producer.send(args.topic, value=message, key=key_bytes)
        print(f"Sent message {i + 1}: {message}")
        time.sleep(args.pause_ms / 1000.0)

    producer.flush()
    producer.close()


if __name__ == '__main__':
    main()
