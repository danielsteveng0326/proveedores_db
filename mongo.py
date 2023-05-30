import pymongo

cl = pymongo.MongoClient("mongodb://localhost:27017/")
print(cl.list_database_names())