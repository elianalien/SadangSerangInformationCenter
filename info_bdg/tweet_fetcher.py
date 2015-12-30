from datetime import datetime, timedelta
import json
from operator import itemgetter
import threading
import time

import tweepy
from tweepy import OAuthHandler

from utils import *

class TweetFetcher(object):
    consumer_key='t09Bj4zaKIjOOgJyCakJoQXPX'
    consumer_secret='pmTmQ0ggVzg72iofoN6PMLuWr8s3TTA4xYVbw7a0dNNTGRS7iH'
    access_token='2910905401-6HhFWEqG4QsypFRgloSa6VM5pMfleH91sEw7T5r'
    access_token_secret='DLVzAUIMDvOj5i16yZsqaL3Ie4F2usdGvcpU9EwQHHRfc'

    #auth method
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    #autentikasi
    api = tweepy.API(auth)

    #list accounts dan id-nya
    accnts = []
    accntIDs = []

    accnts.append(('@ridwankamil', 80323736))
    accnts.append(('@odedmd', 1319572040))
    accnts.append(('@2Serang',1903129470))
    accnts.append(('@diskominfobdg', 1933882213))

    accnts.append(('@persibofficial', 174362532))
    accnts.append(('@simamaung', 80528320))
    accnts.append(('@officialvpc', 114668227))

    accnts.append(('@infobandung', 74081981))
    accnts.append(('@infobdg', 101494663))
    accnts.append(('@lokerbdg', 136212383))

    tweetCount = 20
    # tweetCount = 5
    maxSavedTweets = 50

    #list keywords
    keywords = []
    keywords.extend(['lowongan', 'pekerjaan'])
    keywords.extend(['persib', 'bobotoh', 'viking'])
    keywords.extend(['pembangunan', 'mou', 'anggaran', 'ground breaking'])
    keywords.extend(['perda', 'uu', 'undang', 'izin'])
    keywords.extend(['sadang serang'])

    hashtags = []
    hashtags.extend(['#loker', '#lowker', '#persibday'])

    #list tweets
    tweetDatasDict = {}

    def __init__(self, tweetContainer):

        thread = threading.Thread(target=self.fetch_tweet, args=())
        # Daemonize thread
        thread.daemon = True
        # Start the execution
        thread.start()
        self.tweetContainer = tweetContainer

    #metode ambil tweet yg belum diambil dari account
    def get_accnts_tweets (self):
        #create new tweet data to list new tweets
        self.tweetDatasDict["_new_"] = []

        for (accntName, accntID) in self.accnts:
            self.process_new_tweets(accntName, accntID)

        #sort the new tweets by time
        self.tweetDatasDict["_new_"] = sorted(self.tweetDatasDict["_new_"], key=itemgetter('tweet_id'), reverse=True)

        #filter the new tweets
        self.filter_tweets()

        #save newTweets ke home
        if len(self.tweetDatasDict["_new_"]) > 0:
            self.file_to_object("_home_")
            self.tweetDatasDict["_home_"] = self.tweetDatasDict["_new_"] + self.tweetDatasDict["_home_"]

            self.save_tweets("_home_")
            print "---------- ", len(self.tweetDatasDict["_new_"]), " new tweet fetched ----------"
        else:
            print "---------- no new tweets ----------"


    #metode:
    # ambil tweet yg belum diambil
    # masukin hasilnya ke tweetDatasDict
    # filter hasilnya
    # rewrite file
    def process_new_tweets (self, name, accntID = -1):
        print " processing " + name

        # open saved tweets from file
        self.file_to_object(name)

        print "  fetching from " + name

        # ambil tweet yg belum diambil
        try:
            tweetRawDatas = self.api.user_timeline(user_id=accntID, count = self.tweetCount, since_id=self.get_last_tweet_id(name))
        except:
            print "tweet limit reached at " + datetime.now().strftime('%H:%M:%S')

        print "  got " + str(len(tweetRawDatas)) + " new tweets"

        # simplify tweets
        tweetDatas = self.simplify_tweet(tweetRawDatas)

        # add new tweets to home
        print "  adding newest tweets to home"
        if len(tweetDatas)>0:
            self.tweetDatasDict["_new_"] = tweetDatas + self.tweetDatasDict["_new_"]

        # rewrite file
        print "  joining to previous tweets"
        self.tweetDatasDict[name] = tweetDatas + self.tweetDatasDict[name]
        self.save_tweets(name)

    #open file and convert it to object and save it to tweetDatasDict
    def file_to_object(self, name):
        print "  opening saved tweets from " + name

        #create the file if it doesn't exit
        try:
            tweetsJSONFile = open("info_bdg/content/" + name + ".txt")
            tweetsJSON = tweetsJSONFile.read()
            tweetsJSONFile.close()
        except:
            print name + ".txt file created"
            tweetsJSON = "[]"

        try:
            tweetDatas = json.loads(tweetsJSON)
        except:
            tweetDatas = json.loads("[]")

        tweetDatas = byteify(tweetDatas)

        #check if the name of the tweet data exist, and either replace it or create a new one
        if (name in self.tweetDatasDict) == False:
            self.tweetDatasDict[name] = []

        self.tweetDatasDict[name] = tweetDatas

    #get last tweet from a tweetDatas
    def get_last_tweet_id (self, name):
        tweetDatas = self.tweetDatasDict[name]

        # parse text file
        if len(tweetDatas) > 0:
            print "   last checked at " + tweetDatas[0]["created_at"]
            return tweetDatas[0]["tweet_id"]
        else:
            print "   this source hasn't been checked before"
            return 1

    # remove unused fields from the tweet and return in the form ready to be added to tweetDatasDict
    def simplify_tweet (self, rawData):
        print "  simplifying tweets"

        simplifiedTweets = []
        for j in xrange(len(rawData)):
            tweet = rawData[j]
            simplifiedTweets.append({})
            #convert time
            createdAt = tweet.created_at
            createdAt += timedelta(0, 25200) # from UTC to local

            #get urls
            urls = []
            if 'urls' in tweet.entities:
                for url in tweet.entities['urls']:
                    urls.append({'url' : url['expanded_url'],
                                 'start' : url['indices'][0],
                                 'end' : url['indices'][1]
                                 })

            #get hashTags
            hashTags = []
            if 'hashtags' in tweet.entities:
                for hashtag in tweet.entities['hashtags']:
                    hashTags.append({'text' : hashtag['text'],
                                     'start' : hashtag['indices'][0],
                                     'end' : hashtag['indices'][1]
                                    })

            #get medias
            medias = []
            if 'media' in tweet.entities:
                for media in tweet.entities['media']:
                    medias.append({'url' : media['media_url_https'],

                                    'med_width' : media['sizes']['medium']['w'],
                                    'med_height' : media['sizes']['medium']['h'],

                                    'lrg_width' : media['sizes']['large']['w'],
                                    'lrg_height' : media['sizes']['large']['h']
                                    })

            #save to new simplified dict
            simplifiedTweets[j] = ({'user_id' : tweet.user.id_str,
                                'user_name' : tweet.user.name,
                                'screen_name' : tweet.user.screen_name,
                                'profile_image' : tweet.user.profile_image_url,
                                'created_at' : createdAt.strftime('%Y-%m-%d %H:%M:%S'),
                                'text' : tweet.text,
                                'tweet_id' : tweet.id_str,
                                'urls' : urls,
                                'hashtags' : hashTags,
                                'media' : medias
                                })

        print "   done simplifying"
        return simplifiedTweets

    # metode masukin yg baru, hapus > max saved tweets, dan save hasilnya
    def save_tweets(self, name):
        # hapus >50
        while len(self.tweetDatasDict[name])>self.maxSavedTweets:
            print "   deleting old tweets"
            self.tweetDatasDict[name].pop(self.maxSavedTweets)

        # save hasilnya
        print "   saving " + name + " file"

        f = open('info_bdg/content/' + name + '.txt', 'w')
        f.write(json.dumps( self.tweetDatasDict[name]))
        # print "---------------------"
        # print json.dumps(tweetObjects, indent=2)

    #metode filter tweet dari new tweets (sementara di _home_) dan masukin hasilnya ke keywordsTweets
    def filter_tweets (self):

        print "  filtering tweets"

        for keyword in self.keywords:
            filteredTweetDatas = []
            print "   filtering for " + keyword
            for tweetData in self.tweetDatasDict["_new_"]:
                if (tweetData["text"].lower().find(keyword) >= 0):
                    filteredTweetDatas.append(tweetData)
                    print "     found from " + tweetData["text"]

            #check if the name of the tweet data exist, and either replace it or create a new one
            if (keyword in self.tweetDatasDict) == False:
                self.tweetDatasDict[keyword] = []

            #finally save the filtering result
            if len(filteredTweetDatas) > 0:
                print "     joining to previous filtered tweets"
                self.tweetDatasDict[keyword] = filteredTweetDatas + self.tweetDatasDict[keyword]
                self.save_tweets(keyword)
            else:
                print "    keyword not found"

        for hashtag in self.hashtags:
            filteredTweetDatas = []
            print "   filtering for " + keyword
            for tweetData in self.tweetDatasDict["_new_"]:
                for savedHashtag in tweetData["hashtags"]:
                    if savedHashtag == hashtag:
                        filteredTweetDatas.append(tweetData)
                        print "     found from " + tweetData["text"]

            #check if the name of the tweet data exist, and either replace it or create a new one
            if (keyword in self.tweetDatasDict) == False:
                self.tweetDatasDict[keyword] = []

            #finally save the filtering result
            if len(filteredTweetDatas) > 0:
                print "     joining to previous filtered tweets"
                self.tweetDatasDict[keyword] = filteredTweetDatas + self.tweetDatasDict[keyword]
                self.save_tweets(keyword)
            else:
                print "    hashtag not found"

    # -----MULAI PANGGIL FUNCTION-----

    def fetch_tweet(self):
        """ Method that runs forever """
        while True:
            print "---------- starting fetch process ----------"
            print "at " + datetime.now().strftime('%H:%M:%S')
            self.get_accnts_tweets()
            self.tweetContainer.update()

            time.sleep(120)

# tweetFetcher = TweetFetcher()
# tweetFetcher.fetch_tweet()
