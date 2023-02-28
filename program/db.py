import pymongo

from config import MONGO_URL

myclient = pymongo.MongoClient(MONGO_URL)
mydb = myclient["mydatabase"]
mycol = mydb["customers"]
# mycol.drop()
# mydict = { "name": "John", "address": "Highway 37" }

# x = mycol.insert_one(mydict)
# # print(myclient.list_database_names())