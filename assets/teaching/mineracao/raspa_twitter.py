import json
import tweepy

# credentials
consumer_key = "xxx"
consumer_secret = "xxx"
access_token = "xxx"
access_token_secret = "xxx"

class listener(tweepy.streaming.StreamListener):
    def on_data(self, data):
        data = json.loads(data)
        print data
#        print data["created_at"]
#        print data["favorited"]
#        print data["retweeted"]
        if "place" in data:
            print data["place"]
#        print data["place"]
#        print data["place"]["country_code"]
#        raw_input()
        return True
        
    def on_error(self, status):
        print status

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

while True:
    try:

        twitterStream = tweepy.Stream(auth, listener())
        twitterStream.filter(track = [u"python"])

# outras opcoes de filtro (idioma, local, etc):
# https://dev.twitter.com/streaming/overview/request-parameters

    except:
        continue