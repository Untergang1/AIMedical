from pymongo.mongo_client import MongoClient
from transformers import BertForMaskedLM, BertTokenizer
import torch

from log import get_logger

logger = get_logger(__name__)


class EmbeddingModel:
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained("IDEA-CCNL/Erlangshen-TCBert-330M-Sentence-Embedding-Chinese")
        self.model = BertForMaskedLM.from_pretrained("IDEA-CCNL/Erlangshen-TCBert-330M-Sentence-Embedding-Chinese")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def get_embedding(self, data):
        with torch.no_grad():
            data_input = self.tokenizer(data, return_tensors="pt", padding=True).to(self.device)  # 数据也要移动到GPU
            data_output = self.model(**data_input, output_hidden_states=True)
            embedding = torch.mean(data_output.hidden_states[-1], dim=1).squeeze()
            return embedding.tolist()


mongodb_port = 34861


class MedicalDatabase:
    def __init__(self):
        uri = f"mongodb://localhost:{mongodb_port}/?directConnection=true&serverSelectionTimeoutMS=2000"
        self.client = MongoClient(uri)
        self.client.admin.command("ping")
        self.collection = self.client['medical_db']['medical_knowledge']

        self.embedding_model = EmbeddingModel()

    def get_query_results(self, query):
        query_embedding = self.embedding_model.get_embedding(query)

        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "queryVector": query_embedding,
                    "path": "embedding",
                    "exact": True,
                    "limit": 5
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "instruction": 1,
                    "input": 1,
                    "output": 1,
                    "score": {
                        "$meta": "vectorSearchScore"
                    }
                }
            },
            {
                "$match": {
                    "score": {"$gt": 0.75}
                }
            },
            {
                "$addFields": {
                    "result": {
                        "$concat": [
                            "主题：",
                            "$instruction",
                            "\n患者描述：",
                            "$input",
                            "\n医生诊断：",
                            "$output",
                            "\n"
                        ]
                    }
                }
            }
        ]

        results = self.collection.aggregate(pipeline)
        results = [{'text': item['result'], 'score': item['score']} for item in results]
        logger.debug(results)
        return results


