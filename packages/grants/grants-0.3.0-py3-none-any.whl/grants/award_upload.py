from pymongo import MongoClient
import json
import sys

def main():
    data = json.load(sys.stdin)
    client = MongoClient("localhost", 27017)
    
    assert isinstance(data, list)
    if not data:
        return 
    db = client.ovcri
    for d in data:
        
        if db.awards.count_documents({ "_id": d["_id"] }, limit=1) == 0:
            db.awards.insert_one(d)
        
if __name__ == "__main__":
    main()

