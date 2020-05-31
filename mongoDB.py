import pymongo

from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://admin:54321@clusterpv-stcgg.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = cluster["test"]
collection = db["test"]

#post = {"name":"Sakkigoni","img":"https://i.ytimg.com/vi/7qlKSxwkIVo/hqdefault.jpg","type":"E","id":"sakkigoni","seasons":[]}

#collection.insert_one(post)
#results = collection.find({"name":"user1"})

#for result in results:  print(result)

collection.update_one({"id":"sakkigoni"}, {'$push': {'seasons': {'season':1, 'episodes':{}}}})