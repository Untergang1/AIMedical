import os
import json

from pymongo.mongo_client import MongoClient
from pymongo.operations import SearchIndexModel
from transformers import BertForMaskedLM, BertTokenizer
import torch
import pandas as pd


uri = f"mongodb://localhost:35533/?directConnection=true&serverSelectionTimeoutMS=2000"

client = MongoClient(uri)
client.admin.command("ping")

collection = client['medical_db']['medical_knowledge']

tokenizer = BertTokenizer.from_pretrained("IDEA-CCNL/Erlangshen-TCBert-330M-Sentence-Embedding-Chinese")
model = BertForMaskedLM.from_pretrained("IDEA-CCNL/Erlangshen-TCBert-330M-Sentence-Embedding-Chinese")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


def get_embedding(data):
    with torch.no_grad():
        data_input = tokenizer(data, return_tensors="pt", padding=True).to(device)  # 数据也要移动到GPU
        data_output = model(**data_input, output_hidden_states=True)
        embedding = torch.mean(data_output.hidden_states[-1], dim=1).squeeze()
        return embedding.tolist()


filename = "medical_knowledge.json"

if not os.path.exists(filename):
    df = pd.read_json(
        "hf://datasets/Roselia-penguin/train_medical-dialogue-Chinese/remaining_medical_dialogue_data.json", lines=True)
    df.to_json("medical_knowledge_m.json", orient="records", lines=False, force_ascii=False)

with open(filename, "r", encoding="utf-8") as file:
    data = json.load(file)

batch_size = 2000
for i in range(0, len(data), batch_size):
    batch = data[i:i+batch_size]
    instructions = [item["instruction"] for item in batch]
    embeddings = get_embedding(instructions)
    for item, embedding in zip(batch, embeddings):
        item["embedding"] = embedding

    collection.insert_many(batch)  # 批量插入
    print(f"已插入第 {i // batch_size + 1} 批数据")

# 建立索引
search_index_model = SearchIndexModel(
  definition={
    "fields": [
      {
        "type": "vector",
        "path": "embedding",
        "similarity": "cosine",
        "numDimensions": 1024
      }
    ]
  },
  name="vector_index",
  type="vectorSearch",
)
collection.create_search_index(model=search_index_model)

