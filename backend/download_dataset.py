import pandas as pd

df = pd.read_json("hf://datasets/Roselia-penguin/train_medical-dialogue-Chinese/remaining_medical_dialogue_data.json", lines=True)

df.to_json("medical_knowledge_m.json", orient="records", lines=False, force_ascii=False)