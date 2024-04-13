from pymongo import MongoClient
import certifi


def get_db_handle(db_name, uri):
    client = MongoClient(uri,
                         tls=True,  # Use tls instead of ssl
                         tlsCAFile=certifi.where())  # Ensure SSL certificates are properly handled
    db_handle = client[db_name]
    return db_handle, client
