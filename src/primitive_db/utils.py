import json


def load_metadata(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        #print("Такого файла не существует")
        return {}

def save_metadata(filepath, data):
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file,ensure_ascii=False, indent=4)

load_metadata("db_meta.json")
data = {{
    "type": "Person",
    "text": "Hayden Panettiere",
    "start": 0,
    "end": 17,
    "confidence": 0.9986
  },
  {
    "type": "Job Title",
    "text": "actress",
    "start": 68,
    "end": 75,
    "confidence": 0.8307
  },
  {
    "type": "Organization",
    "text": "coroner",
    "start": 156,
    "end": 163,
    "confidence": 0.9512
  },
  {
    "type": "Job Title",
    "text": "actress",
    "start": 257,
    "end": 264,
    "confidence": 0.9013
  },
  {
    "type": "Person",
    "text": "Hayden Panettiere",
    "start": 265,
    "end": 282,
    "confidence": 0.9924
  }}
data
save_metadata("db_meta.json", data)