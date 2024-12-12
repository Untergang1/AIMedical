from pymongo.mongo_client import MongoClient
from typing import Dict


class UserDatabase:
    def __init__(self):
        uri = f"mongodb://localhost:35533/?directConnection=true&serverSelectionTimeoutMS=2000"
        self.client = MongoClient(uri)
        self.client.admin.command("ping")
        self.collection = self.client['user_db']['user_info']

    def query_name(self, username: str):
        result = self.collection.find_one({"username": username})
        return result

    def insert_user(self, user_info: Dict):
        query_filter = {'username': user_info['username']}
        operation = {"$set": user_info}
        result = self.collection.update_one(
            query_filter,
            operation,
            upsert=True
        )

        if result.matched_count == 0 and result.upserted_id:
            return True
        else:
            return False

    def verify_usr(self, login_message: Dict):
        result = self.collection.find_one(login_message)
        if result:
            return True
        else:
            return False
