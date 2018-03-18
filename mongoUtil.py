from pymongo import MongoClient


#  db.createCollection(name, options)



class MongoUtils:

    def __init__(self, address, port, database_name, collection_name):
        self.address = address
        self.port = port
        self.database_name = database_name
        self.collection = collection_name
        self.db = self.getDB()

    def checkCollectionExists(self, collection_name):
        flag = collection_name in self.db.collection_names()
        return flag

    def createCollection(self, collection_name):
        self.db.create_collection(collection_name)

    def addSampleDataToCollection(self):
        self.insertData({'ImageURL' : 'test_url_goes_here',
                         'IsDownloaded': '1',
                         'DownloadDate': ''})

    def addUniqueConstraintToCollection(self, parameter):
        # // https://docs.mongodb.com/manual/core/index-unique/
        # self.db[self.collection].createIndex("{\"" + parameter + "\": 1},{unique: true}")
        self.db[self.collection].create_index(parameter, unique=True)

    def getDB(self):
        # creating connections for communicating with Mongo DB
        client = MongoClient(self.address, self.port)
        # client = MongoClient('localhost:27017')
        db = client[self.database_name]
        return db

    def insertData(self, jsonFile):
        try:
            #  Names can be dynamic too :     https://stackoverflow.com/a/24800102
            # db.GentlemenSpeak.insert_one(jsonFile)
            self.db[self.collection].insert_one(jsonFile)
        except Exception as e:
            print str("Exception in json Insert : " + str(e))


    def update(self, jsonFile):
        pass

    # This works!!!!  hahahahahahhahahhahahahaaaaaaa
    def updateAllWithoutCondition(self, parameter, parameterValue):
        # https://stackoverflow.com/a/23347140
        self.db[self.collection].update_many({},
        {'$set': {parameter:parameterValue}})

    # This works!!!!  hahahahahahhahahhahahahaaaaaaa
    def updateManyWithCondition(self,parameter,parameterValue):
        # https://stackoverflow.com/a/23347140
        self.db[self.collection].update_many({},
        {'$set': {parameter: parameterValue}})


# Exception in json Insert : E11000 duplicate key error collection: Collection.GentlemenSpeak index: ImageURL_1 dup key: { : "https://78.media.tumblr.com/b589a083384792c3e9d1857c46125d73/tumblr_p5dfhclSzC1r52xqyo1_1280.jpg" }
# Exception in json Insert : E11000 duplicate key error collection: Collection.GentlemenSpeak index: ImageURL_1 dup key: { : "https://78.media.tumblr.com/1fa59acc25bb10794411501dd6ccacd5/tumblr_p5bf8d1gfd1r52xqyo1_1280.jpg" }
# Exception in json Insert : E11000 duplicate key error collection: Collection.GentlemenSpeak index: ImageURL_1 dup key: { : "https://78.media.tumblr.com/adad29456235224fb1c6d74faf3c8107/tumblr_p58ssjTU2K1r52xqyo1_1280.jpg" }



