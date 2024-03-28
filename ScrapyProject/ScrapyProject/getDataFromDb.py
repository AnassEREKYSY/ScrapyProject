import sys
import pymongo
from settings import MONGODB_URI, MONGODB_DB

def getDataFromDb(collection_name):
    # Retrieve MongoDB URI and database name from settings
    mongo_uri = MONGODB_URI
    mongo_db = MONGODB_DB
    
    # Connect to MongoDB
    client = pymongo.MongoClient(mongo_uri)
    db = client[mongo_db]

    # Access the specified collection
    collection = db[collection_name]
    
    # Print data from the collection
    print(f"Data for {collection_name}:")
    for item in collection.find():
        print(item)

    # Close the MongoDB connection
    client.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python retrieve_data.py <collection_name>")
        sys.exit(1)

    collection_name = sys.argv[1]
    getDataFromDb(collection_name)
