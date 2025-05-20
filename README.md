Brieffing:
---
  Messages are created using Kafka Producer, which allows to set a Kafka Topic. Additional Kafka Admin configuration allows to set a number of partitions.
  
  To simulate multiple nodes, a Kafka Consumer is created in different threads, where each Kafka Consumer reads different messages using partitions. Those partitions ae handled automatically by Kafka.
  
  The readed messages are stored in a list, and every number of seconds, the messages are saved in batch into a MongoDB collection and the list is cleared.
  
  PyMongo allows to get unique elements and count them, so further processing is not needed.
  
  Finally, following methods are exposed in FastAPI: Timestamp Parsing, Count unique IP's

Instructions:
---
  - Install MongoDB
  - Install Apache Kafka locally or using a Docker Image
  - If using Docker image, run a container using:
    "docker run -p 9092:9092 apache/kafka:4.0.0"
  - Install additional Python libraries:
    - FastAPI: https://fastapi.tiangolo.com/
    - PyMongo: https://pymongo.readthedocs.io/en/stable/
    - Kafka Python: https://kafka-python.readthedocs.io/en/master/ 
  - Send messages using "python kafka_sender.py"
  - Read messages using "python kafka_receiver.py"
  - Run FastAPI server using "fastapi dev main.py"
  - Open this link in browser "http://127.0.0.1:8000/docs" to explore available endpoints

Potential Challenges and Solutions
---
  - Build a better real-time data pipelines
  - Set an accurate number of the batch size for saving messages based on time frequency and payload of the messages 
  - Increase the number of partitions according to the number of messages received
  - Design a distributed architecture to handle data in different nodes

Screenshots:
---
  - Messages are sent, but each message is readed by a different Kafka Consumer created in each thread
    ![image](https://github.com/user-attachments/assets/b77cee1b-9516-43b1-b7f3-311cc2197806)
    ![image](https://github.com/user-attachments/assets/a77a9bfd-5ba4-4fd5-a7b2-646b8b3df6b6)
  - Messages saved in MongoDB
    ![image](https://github.com/user-attachments/assets/e87927de-f111-4478-849b-39d72bfdffdd)
  - Endpoints are deployed to read data saved in MongoDB
    ![image](https://github.com/user-attachments/assets/52be2360-5b55-40b3-ac0b-473096e114fc)
  - Endpoint are deployed to format timestamp
    ![image](https://github.com/user-attachments/assets/bfc8f7fd-aed6-4a68-81b5-05f0613261ec)




