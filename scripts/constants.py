# pylint: skip-file

import pymongo

MONGO_SERVER = "localhost"
MONGO_PORT = "27016"
MONGO_CLIENT = pymongo.MongoClient(f"mongodb://mongoadmin:talkischeapshowmethecode@{MONGO_SERVER}:{MONGO_PORT}/jsonschemadiscovery?authSource=admin")
MONGO_DB = "jsonschemadiscovery"
API_URL = "http://localhost:4200/api"
API_STEPS_ALL = f"{API_URL}/batch/rawschema/steps/all"
USERNAME = "testuser"
PASS = "testpass"
EMAIL = "a@b.com"
DATA_FOLDER = "dataset"

# API params
ADDRESS = "mongodb"
PORT = "27017"
DATABASENAME = "jsonschemadiscovery"
AUTH_DATABASE = "admin"
AUTH_MECHANISM = "SCRAM-SHA-1"
USERNAME = "mongoadmin"
PASSWORD = "talkischeapshowmethecode"
