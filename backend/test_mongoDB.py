import os

from pymongo.mongo_client import MongoClient

password = os.getenv("MONGODB_PASSWORD")

uri = f"mongodb+srv://untergang404:{password}@cluster0.uoe4l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)

collection = client['sample_mflix']['movies']

result = collection.find({"year": 1903})
print(f"Result: {result}")
