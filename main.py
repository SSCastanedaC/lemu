from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from time_formatter import format_datetime
from settings import MONGO_URL, MONGO_DB, MONGO_COLLECTION
from typing import Tuple, Dict

app = FastAPI()
client = MongoClient(MONGO_URL)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]


@app.get("/")
def read_root() -> Dict:
    """
    Returns static dict

    Parameters:
    - None

    Return:
    - response (dict)
    - status_code (int)
    """
    return {
        "Developer": "Sebastián Castañeda"
    }

@app.get("/time/formatter/{time_str}")
def format_time(time_str: str) -> Dict:
    """
    Returns the time in ISO format

    Parameters:
    - time_str (str): Timestamp with inconsistent format

    Return:
    - response (dict)
    - status_code (int)
    """
    try:
        time_str = format_datetime(time_str)
        return {"time": time_str}
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@app.get("/count/addresses")
def count_addresses() -> Dict:
    """
    Returns the name of distinct IP addresses saved on DB

    Parameters:
    - None

    Return:
    - responde (dict)
    - status_code (int)
    """
    total_addresses = collection.count_documents({})
    unique_addresses = len(collection.distinct("ip_address"))
    return {
        "total_addresses,": total_addresses,
        "unique_addresses": unique_addresses
    }
