from typing import Dict
from datetime import datetime

from pymongo.mongo_client import MongoClient


mongodb_port = 34861


class UserDatabase:
    def __init__(self):
        uri = f"mongodb://localhost:{mongodb_port}/?directConnection=true&serverSelectionTimeoutMS=2000"
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

    def update_user(self, user_info: Dict):
        query_filter = {'username': user_info['username']}
        operation = {"$set": user_info}
        result = self.collection.update_one(
            query_filter,
            operation,
            upsert=False
        )

        if result.matched_count == 0:
            return False
        else:
            return True

    def verify_usr(self, username: str, password: str) -> (bool, str):
        user = self.collection.find_one({'username': username})
        if not user:
            return False, "用户不存在"
        else:
            if user['password'] == password:
                return True, "登录成功"
            else:
                return False, "密码错误"

    def insert_medical_record(self, username: str, query: str, response: str):
        time = datetime.now().strftime("%Y_%m_%d")
        new_record = {
            'time': time,
            'query': query,
            'response': response
        }
        self.collection.update_one(
            {'username': username},
            {'$push': {'medical_records': new_record}}
        )



