from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["phishing_detection"]

collection = db["logs"]

print("MongoDB Connected Successfully")