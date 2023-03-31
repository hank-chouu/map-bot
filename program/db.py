import pymongo

from program.config import MONGO_URL

class Mongo_object(object):

    def __init__(self):

        client = pymongo.MongoClient(MONGO_URL, connect=False)
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
    
    def reset_user(self, user_id):

        query = {'id': user_id}
        update = {"$set": {'status':0,'params':{}}}
        x = self.collection.update_one(query, update)
        return x
       
    def start_search(self, user_id):

        query = {'id': user_id}
        update = {"$set": {'status': 1}}
        x = self.collection.update_one(query, update)
        return x         
    
    def save_keyword(self, user_id, keyword):

        query = {'id': user_id}
        update = {"$set": {'params':{'keyword': keyword}, 'status': 2}}
        x = self.collection.update_one(query, update)
        return x
    
    def save_location(self, user_id, latitude, longitude):

        query = {'id': user_id}
        result = self.collection.find(query)
        params = {}
        for res in result:
            params = res['params']
        params['latitude'] = str(latitude)
        params['longitude'] = str(longitude)
        update = {'$set': {'status':3, 'params':params}}
        x = self.collection.update_one(query, update)
        return x

    
    def get_status(self, user_id):
        query = {'id': user_id}
        result = self.collection.find(query)
        for res in result:
            return res['status']
        
    def get_params(self, user_id):
        query = {'id': user_id}
        result = self.collection.find(query)
        for res in result:
            return res['params']

    def is_user_exists(self, user_id):

        query = {'id':user_id}
        result = self.collection.find(query)
        if len(list(result)) == 1:
            return True
        else:
            return False
        
    def get_users_count(self):
        count = self.collection.count_documents({})
        return count
       
Mongo = Mongo_object()
