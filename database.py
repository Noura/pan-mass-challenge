from pymongo import MongoClient

def get_database():
    mongo = getattr(MongoClient('localhost', 27017), 'panmass')
    return DB(mongo)

class DB(object):
    def __init__(self, mongo):
        self.mongo = mongo
    
    def add_photo(self, filename, caption, user, desc):
        self.mongo.photos.insert({
            'filename': filename,
            'caption': caption,
            'user': user,
            'desc': desc
        })

    def delete_photo(self, pid):
        self.mongo.photos.remove({'_id':pid})

    def get_photos(self):
        return self.mongo.photos.find()
