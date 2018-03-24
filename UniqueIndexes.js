db.getCollection('GentlemenSpeak').find({})

// https://docs.mongodb.com/manual/core/index-unique/
db.GentlemenSpeak.createIndex( { "ImageURL": 1 }, { unique: true } )

// https://docs.mongodb.com/manual/reference/method/db.collection.getIndexes/
db.GentlemenSpeak.getIndexes()