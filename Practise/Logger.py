import json

def log(obj):
    print(json.dumps(obj, encoding='UTF-8', ensure_ascii=False))