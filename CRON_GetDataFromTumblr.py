# https://github.com/tumblr/pytumblr
# pip install pytumblr
# pip install pymongo

import datetime
import json
import logging
import re
import ConfigParser

import pytumblr

from mongoUtil import MongoUtils

##############################################################################################
###############        Collecting Connections and Resources
##############################################################################################

# Source : https://docs.python.org/2/howto/logging.html
logging.basicConfig(filename='pytumblr.log',
                    format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    datefmt='%m/%d/%Y %I:%M:%S %p')

# Initialize the Config file
config = ConfigParser.RawConfigParser()
config.read('config.properties')

# Authenticate this via OAuth
key = config.get('Keys', 'keys.consumerKey')
secret = config.get('Keys', 'keys.consumerSecret')
client = pytumblr.TumblrRestClient(key, secret)

# Initialize DataBase
ADDRESS = config.get('DatabaseSection', 'database.address')
PORT = int(config.get('DatabaseSection', 'database.port'))
DATABASE = config.get('DatabaseSection', 'database.database')

PAGE_NAME = 'sabyaasachi'
COLLECTION_NAME = PAGE_NAME

##############################################################################################
###############        Placing guns on the board: Defining functions
##############################################################################################

def logAndPrint(message):
    logging.info(message)
    print message

def logAndPrintError(message):
    logging.error(message)
    print message

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

        # nophotosPosted = len(posts['posts'][i]['photos'])
        # print 'Summary is : ' + posts['posts'][i]['caption'].encode('utf-8') + posts['posts'][i]['slug'].encode('utf-8')
        # print 'Photos in ' + str(i) + 'th post : ' + str(nophotosPosted)
        # print 'Tags are : ' + str(posts['posts'][i]['tags'])
        # print ''
        # print ''

        if (type == 'photo'):
            count = len(posts['posts'][i]['photos'])

            j = 0
            for j in range(count):
                # print 'For post :' + str(i)
                # print 'Summary is : ' + posts['posts'][i]['caption'].encode('utf-8') + posts['posts'][i]['slug'].encode('utf-8')
                # dict = posts['posts'][i]['photos']
                # url = posts['posts'][i]['photos'][j]['original_size']['url']
                # print "URL " + str(j) + " is :" + str(url)
                # print ''
                # print ''
                # print ''

                jsonBody = {
                    'Source': posts['blog']['url'],
                    'PostURL': posts['posts'][i]['post_url'],
                    'ShortDescription': posts['posts'][i]['slug'],
                    'Tags': posts['posts'][i]['tags'],
                    'ContentType': posts['posts'][i]['type'],
                    'ImageURL': posts['posts'][i]['photos'][j]['original_size']['url'],
                    'SummaryFromSource': posts['posts'][i]['caption'].encode('utf-8'),
                    'postedDate': posts['posts'][i]['date'],
                    'grabbedDate': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'IsDownloaded': '',
                    'DownloadDate': ''
                }
                # Now insert
                mongo.insertData(jsonBody)
            return


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
            # Now insert
            mongo.insertData(jsonBody)
            return

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
            # Now insert
            mongo.insertData(jsonBody)
            return

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
            # Now insert
            mongo.insertData(jsonBody)

    except Exception as e:
        # print e
        print "Exception in method mongoInsert : " + str(e).encode('utf-8') + " at here : " + posts['posts'][i]['post_url']


# Make the request
# clientInfo = client.info()
# following =  client.following()
# print json.dumps(following, sort_keys=True, indent=3)

postLimit = 50
j = 0

total_posts = client.posts(PAGE_NAME, limit = 2)['total_posts']
print 'Total posts : ' + str(total_posts)

mongo = MongoUtils(ADDRESS, PORT, DATABASE, COLLECTION_NAME)

# check if collection is available
print "Existence flag : " + str(mongo.checkCollectionExists(COLLECTION_NAME))
if not mongo.checkCollectionExists(COLLECTION_NAME):
    mongo.createCollection(COLLECTION_NAME)
    mongo.addSampleDataToCollection()
    mongo.addUniqueConstraintToCollection('ImageURL')

for j in xrange(j, total_posts, postLimit):
    print "Getting from index : " + str(j) + " to " + str(j+postLimit)
    posts = client.posts(PAGE_NAME, limit=postLimit, offset=j + 1)

    # print "************************************************************"
    # print json.dumps(posts, sort_keys=True, indent=2)
    # print "************************************************************"

    for i in range(postLimit):
        try:
            if(posts['posts'][i]):
                mongoInsert(posts, i)
        except Exception as e:
            if 'list index out of range' in str(e):
                pass
            else:
                logAndPrintError("From GetDataFromTumblr[dot]py : " + str(e))












