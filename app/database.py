from pymongo import MongoClient

client = MongoClient("mongodb://mongodb")
db = client["router_app"]
logs_collection = db["logs"]
destinations_collection = db["destinations"]
strategy_collection = db["strategy"]
