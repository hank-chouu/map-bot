import pymongo

from program.config import MONGO_URL

class Mongo_object(object):

    def __init__(self):

        client = pymongo.MongoClient(MONGO_URL)
        db = client["map_bot"]
        self.collection = db["users"]

    def insert_new(self, user_id):

        new_insert = { 'id': user_id, 'status':0,'params':{}}
        x = self.collection.insert_one(new_insert)
        return x
    
    def delete(self, user_id):

        query = {'id': user_id}
        x = self.collection.delete_one(query)
        return x
    
    def saving_type(self, user_id, search_type):

        query = {'id': user_id}
        update = {"$set": {'params':{'type': search_type}, 'status': 1}}
        x = self.collection.update_one(query, update)
        return x
    
    def saving_location(self, user_id, latitute, longitude):

        query = {'id': user_id}
        result = self.collection.find(query)
        params = {}
        for res in result:
            params = res['params']
        params['latitute'] = str(latitute)
        params['longitute'] = str(longitude)
        update = {'$set': {'status':2, 'params':params}}
        x = self.collection.update_one(query, update)
        return x

    
    def return_status(self, user_id):
        query = {'id': user_id}
        result = self.collection.find(query)
        for res in result:
            return res['status']
    
Mongo = Mongo_object()
