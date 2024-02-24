# pylint: skip-file

import requests
import sys
import os


from constants import MONGO_CLIENT, MONGO_DB, API_URL, USERNAME, PASS, EMAIL, DATA_FOLDER
from experiment1 import perform_experiment1
from experiment2 import perform_experiment2


def get_token():
    print(f"Logging in with username {USERNAME}")
    login_uri = f"{API_URL}/login"
    response = requests.post(login_uri, json={"email": EMAIL, "password": PASS})
    
    if response.status_code == 200:
        print("Login successful")
        return response.json()["token"]
    else:
        print("Login failed")
        print(response.text)
        sys.exit(1)


def register_user():
    print(f"Registering user with username {USERNAME}")
    register_uri = f"{API_URL}/register"
    response = requests.post(register_uri, json={"username": USERNAME, "password": PASS, "email": EMAIL})
    
    if response.status_code == 200:
        print("User registered successfully")
    else:
        print("User registration failed")
        print(response.text)
        sys.exit(1)


def cleanup(db_conn):
    print("Dropping all collections in database")
    collections = db_conn.list_collection_names()

    for collection_name in collections:
        print(f"Dropping collection {collection_name}")
        db_conn[collection_name].drop()

    print("Cleaning json files in dataset directory")
    for root, dirs, files in os.walk(DATA_FOLDER):
        for file in files:
            if file.endswith(".json"):
                os.remove(os.path.join(root, file))


def get_db_connection():
    try:
        # Perform a simple operation: list database names
        MONGO_CLIENT.list_database_names()
        print("Connection to MongoDB server was successful.")
        return MONGO_CLIENT[MONGO_DB]
    except Exception as e:
        print(f"An error occurred while connecting to MongoDB: {e}")
        sys.exit(1)


def perform_experiments(db_conn):
    # cleanup(db_conn)
    # register_user()
    # token = get_token()

    # perform_experiment1(db_conn, token)

    cleanup(db_conn)
    register_user()
    token = get_token()

    perform_experiment2(db_conn, token)


if __name__ == "__main__":
    db_conn = get_db_connection()
    perform_experiments(db_conn)

