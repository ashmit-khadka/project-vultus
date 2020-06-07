import pymongo
from pymongo import MongoClient

def getCollection(collection):
    cluster = MongoClient("mongodb+srv://admin:54321@clusterpv-stcgg.gcp.mongodb.net/test?retryWrites=true&w=majority")
    db = cluster["pv"]
    return db[collection]

#post = {"name":"Sakkigoni","img":"https://i.ytimg.com/vi/7qlKSxwkIVo/hqdefault.jpg","type":"E","id":"sakkigoni","seasons":[]}

#collection.insert_one(post)
#collection = getCollection('pre')
#results = collection.find_one({"name":"Meri Bahhjssai"})
#print(results)
#for result in results:  print(result)

#collection.update_one({"id":"sakkigoni"}, {'$push': {'seasons': {'season':1, 'episodes':{}}}})
