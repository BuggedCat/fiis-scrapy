import urllib.parse

from pymongo import MongoClient


def start_mongo_client():
    host = "localhost"
    port = 27017

    username = "admin"
    password = "admin"

    client = MongoClient(f"mongodb://{username}:{urllib.parse.quote_plus(password)}@{host}:{port}")
    return client


def fetch_documentos_ids(client: MongoClient):
    database = "fiis"
    collection = "fnet_documentos"

    db = client[database]
    collection = db[collection]

    documentos_ativos = collection.find({}, {"id": 1, "_id": 0})
    yield from documentos_ativos
