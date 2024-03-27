import sys
import pymongo
from .settings import MONGODB_URI
from .settings import MONGODB_DB

def getDataFromDb(collection_name):

    mongo_uri = MONGODB_URI
    mongo_db = MONGODB_DB

    
    client = pymongo.MongoClient(mongo_uri)
    db = client[mongo_db]

    collection = db[collection_name]
    print(f"Data for {collection_name}:")
    for item in collection.find():
        print(item)

    client.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python retrieve_data.py <collection_name>")
        sys.exit(1)

    collection_name = sys.argv[1]
    getDataFromDb(collection_name)
