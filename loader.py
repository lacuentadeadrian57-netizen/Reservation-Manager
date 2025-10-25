import json
import os

def save_data(data: dict, filename: str):
    temp = filename + ".tmp"
    try:
        with open(temp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(temp, filename)
        return True
    except:
        try:
            os.remove(temp)
            return False
        except:
            return False
        

def load_data(filename: str):
    if not os.path.exists(filename):
        return None
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)
