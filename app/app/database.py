import os
from pymongo import MongoClient

MONGO_DATABASE_PROTOCOL = os.environ.get("MONGO_DATABASE_PROTOCOL")  # mongodb
MONGO_DATABASE_USER = os.environ.get("MONGO_DATABASE_USER")  # root
MONGO_DATABASE_PASSWORD = os.environ.get("MONGO_DATABASE_PASSWORD")  # root
MONGO_DATABASE_CONTAINER_NAME = os.environ.get(
    "MONGO_DATABASE_CONTAINER_NAME")  # mongo_db
MONGO_DATABASE_PORT = int(os.environ.get("MONGO_DATABASE_PORT"))  # 27017

DATABASE_URL = "%s://%s:%s@%s:%d" % (
    MONGO_DATABASE_PROTOCOL, MONGO_DATABASE_USER, MONGO_DATABASE_PASSWORD, MONGO_DATABASE_CONTAINER_NAME, MONGO_DATABASE_PORT)

client = MongoClient(DATABASE_URL)
db = client.first_test  #database名がfirst_test
