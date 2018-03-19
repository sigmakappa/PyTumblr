# https://github.com/tumblr/pytumblr
# pip install pytumblr
# pip install pymongo

import datetime
import json
import re

import pytumblr

from mongoUtil import MongoUtils


# Method to get all HTML tags removed from a string
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext


'''
Columns taken from here:
        Post Source
        Post URL
        Short Desc (Slug)
        Tags
        Content Type
        Image URL
        Post Summary from Source
        Date Posted
        Post Grabbed Time
'''
def mongoInsert(posts, i):
    try:
        type = posts['posts'][i]['type']



        nophotosPosted = len(posts['posts'][i]['photos'])
        print 'Summary is : ' + posts['posts'][i]['caption'].encode('utf-8')
        print 'Photos in ' + i + 'th post : ' + nophotosPosted



        if (type == 'photo'):
            jsonBody = {
                'Source': posts['blog']['url'],
                'PostURL': posts['posts'][i]['post_url'],
                'ShortDescription': posts['posts'][i]['slug'],
                'Tags': posts['posts'][i]['tags'],
                'ContentType': posts['posts'][i]['type'],
                'ImageURL': posts['posts'][i]['photos'][0]['alt_sizes'][0]['url'],
                'SummaryFromSource': posts['posts'][i]['caption'].encode('utf-8'),
                'postedDate': posts['posts'][i]['date'],
                'grabbedDate': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'IsDownloaded': '',
                'DownloadDate': ''
            }
        if (type == 'link'):
            jsonBody = {
                'Source': posts['blog']['url'],
                'PostURL': posts['posts'][i]['post_url'],
                'ShortDescription': posts['posts'][i]['slug'],
                'Tags': posts['posts'][i]['tags'],
                'ContentType': posts['posts'][i]['type'],
                'LinkedURL': posts['posts'][i]['url'],
                'SummaryFromSource': posts['posts'][i]['reblog']['comment'].encode('utf-8'),
                'postedDate': posts['posts'][i]['date'],
                'grabbedDate': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        if (type == 'text'):
            jsonBody = {
                'Source': posts['blog']['url'],
                'PostURL': posts['posts'][i]['post_url'],
                'ShortDescription': posts['posts'][i]['slug'],
                'Tags': posts['posts'][i]['tags'],
                'ContentType': posts['posts'][i]['type'],
                'SummaryFromSource': posts['posts'][i]['reblog']['comment'].encode('utf-8'),
                'postedDate': posts['posts'][i]['date'],
                'grabbedDate': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        if (type == 'video'):
            jsonBody = {
                'Source': posts['blog']['url'],
                'PostURL': posts['posts'][i]['post_url'],
                'ShortDescription': posts['posts'][i]['slug'],
                'Tags': posts['posts'][i]['tags'],
                'ContentType': posts['posts'][i]['type'],
                'VideoURL': posts['posts'][i]['permalink_url'],
                'SummaryFromSource': posts['posts'][i]['caption'].encode('utf-8'),
                'postedDate': posts['posts'][i]['date'],
                'grabbedDate': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        # mongo.insertData(jsonBody)
        # mongo.updateAllWithoutCondition('newParam', 'defaultValue')
    except Exception as e:
        print e
        # print str("Exception in method mongoInsert : " + e.encode('utf-8') + " at here : " + posts['posts'][i]['post_url'])


# Authenticate via OAuth
client = pytumblr.TumblrRestClient(
  'Qlc7blKjb9sacKRjFOHZpwAhqdGsPxVgfDQ1Tg8TfBrW8dSUXB',
  '1JYw1lrlM3lUWrwXPh7DSEDeaSMZszEdxzza2rgnfGaLDcy6cI',
  'VmL6CeGMdWSXlDjy8azZOPwFbYXlveN6Z8qqje9k80ufKrngNb',
  'KZFkVSywraa0sQN9ovfxSEnt0Fbiligka5ldsjCOyfeOy32q1x'
)

# Make the request
clientInfo = client.info()
following =  client.following()

# print following
# print json.dumps(following, sort_keys=True, indent=3)

postLimit = 50
j = 0



pageName = 'sabyaasachi'
collection_name = 'the_test_collection2'

total_posts = client.posts(pageName, limit = 2)['total_posts']
print 'Total posts : ' + str(total_posts)

mongo = MongoUtils('localhost', 27017, 'Tumblr', collection_name)

# check if collection is available
print "Existence flag : " + str(mongo.checkCollectionExists(collection_name))
if not mongo.checkCollectionExists(collection_name):
    mongo.createCollection(collection_name)
    mongo.addSampleDataToCollection()
    mongo.addUniqueConstraintToCollection('ImageURL')

for j in xrange(j, total_posts, postLimit):
    print "Getting from index : " + str(j) + " to " + str(j+postLimit)
    posts = client.posts(pageName, limit=postLimit, offset=j+1)

    print "************************************************************"
    # print json.dumps(posts, sort_keys=True, indent=2)
    print "************************************************************"

    for i in range(postLimit):
        if(posts['posts'][i]):
            mongoInsert(posts, i)











