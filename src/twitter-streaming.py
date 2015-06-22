#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy.models import BoundingBox
from tweepy import OAuthHandler
from tweepy import Stream

from geocoder import mapquest

import sys, os, json,csv, atexit
import NaiveBayes, BDTokenizer
import happytokenizer

# current workspace os path
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

#loading topic words to an array
topicterms_path = os.path.join(__location__, 'fastfood-terms.csv')
topicterms_file = open(topicterms_path, newline='')
topicterms = list(csv.reader(topicterms_file, delimiter=','))[0]

#Common English stop words list
stopwords_path = os.path.join(__location__, 'stopwords.csv')
stopsowrds_file = open(stopwords_path, newline='')
stopwords = list(csv.reader(stopsowrds_file, delimiter=','))[0]
    
#Variables that contains the user credentials to access Twitter API
# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
access_token = "1202300803-shAA6d9PyghbhVf6B088QjmxhmIdr3aC8uY4ttP"
access_token_secret = "JAi3lggPAptFoPe2G01t938T5A98WitvdCbwlp2PSTyjL"
# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
consumer_key = "yviFZBUfDMLK0Ytck61QVSKCs"
consumer_secret = "H5z6ze7NzvIGV8qCqEb1Q4yxlzLV0PlSnscFKDuu5zjeB9zYrS"

twitter_abbrs=['cc', 'cx', 'ct', 'dm', 'ht', 'mt', 'prt', 'rt','em','ezine','fb','li','seo','sm','smm','smo','sn','sroi','ugc','YT']
TweetsCount = 0
states = {
        '': 0,
        'N/A':0,
        'AK': 0,
        'AL': 0,
        'AR': 0,
        'AS': 0,
        'AZ': 0,
        'CA': 0,
        'CO': 0,
        'CT': 0,
        'DC': 0,
        'DE': 0,
        'FL': 0,
        'GA': 0,
        'GU': 0,
        'HI': 0,
        'IA': 0,
        'ID': 0,
        'IL': 0,
        'IN': 0,
        'KS': 0,
        'KY': 0,
        'LA': 0,
        'MA': 0,
        'MD': 0,
        'ME': 0,
        'MI': 0,
        'MN': 0,
        'MO': 0,
        'MP': 0,
        'MS': 0,
        'MT': 0,
        'NA': 0,
        'NC': 0,
        'ND': 0,
        'NE': 0,
        'NH': 0,
        'NJ': 0,
        'NM': 0,
        'NV': 0,
        'NY': 0,
        'OH': 0,
        'OK': 0,
        'OR': 0,
        'PA': 0,
        'PR': 0,
        'RI': 0,
        'SC': 0,
        'SD': 0,
        'TN': 0,
        'TX': 0,
        'UT': 0,
        'VA': 0,
        'VI': 0,
        'VT': 0,
        'WA': 0,
        'WI': 0,
        'WV': 0,
        'WY': 0
}

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    
    """ A listener handles tweets are the received from the stream.
    """
    def on_data(self, data):
        
        try:
            tweet = json.loads(data, encoding='utf-8')
            self.countTweet(tweet)
            tweet_tokens = BDTokenizer.tokenize(tweet['text'],sentimentTokenizer,stopwords)
            if(self.isTweetGenuine(tweet_tokens) and 
               self.isTweetRelatedFF(tweet)[0] and 
               self.isTweetLocatable(tweet)):
                #print(tweet['text'])
                tweets_file = open('test.json', 'a', encoding='utf-8')
                tweets_file.write(str(tweet))
                tweets_file.close()
                #self.storeTweet(tweet)
                self.storeTweetSentiment(tweet)
        except:
            e = sys.exc_info()[0]
            print( "<p>Error: %s</p>" % e )

    def on_error(self, status):
        print (status)
    
    def countTweet(self, tweet):
        global TweetsCount
        TweetsCount = TweetsCount + 1
        if self.isTweetLocatable(tweet):
            state = getTweetState(tweet)
            if state in states:
                states[state] += 1
        else:
             states['N/A'] += 1
    
    def isTweetLocatable(self, tweet):
        try:
            if (tweet['place']['bounding_box']['type'] in ['Polygon']):
                if(len(tweet['place']['bounding_box']['coordinates'][0]) == 4):
                    return True
            return False
        except:
            print("isTweetLocatable = Error")
            e = sys.exc_info()[0]
            print( "<p>Error: %s</p>" % e )
            return False
    
    def isTweetRelatedFF(self, tweet):
        """
        This will check if tweet is related to our topic (using topic terms).
        """
        try:
            #if tweet has any of topic term accept it as related
            tweet_text = tweet['text'].lower()
            for term in topicterms:
                if  term.lower() in tweet_text:
                    print(term)
                    return (True, term)
        except:
            #e = sys.exc_info()[0]
            #print( "<p>Error: %s</p>" % e )
            print("isTweetFF = Error")
            e = sys.exc_info()[0]
            print( "<p>Error: %s</p>" % e )
            return (False, None)
        return (False, None)
    
    def isTweetRelated(self, tweet_tokens):
        """
        This will check if tweet is related to our topic (using topic terms).
        """
        try:
            #if tweet has any of topic term accept it as related
            #tweet_text = tweet['text'].lower()
            for term in topicterms:
                for token in tweet_tokens:
                    if  term == token:
                        print(term)
                        return (True, term)
        except:
            e = sys.exc_info()[0]
            print( "<p>Error: %s</p>" % e )
            return (False, None)
        return (False, None)
    
    def isTweetGenuine(self, tweet_tokens):
        """
        This will check if tweet is genuinely valuable for our purpose.
        We don't care for tweets which are retweets, spam, comercials, or ...
        """
        try:
            #if tweet has commercial abbreviations or it is a retweet ignore
            #tweet_text = tweet['text'].lower()
            for abbr in twitter_abbrs:
                for token in tweet_tokens:
                    if  abbr == token:
                        return False
        except:
            e = sys.exc_info()[0]
            print( "<p>Error: %s</p>" % e )
            print("isTweetG = Error")
            return False
        return True
    
    def storeTweet(self,tweet):
        try:
            print(str(tweet))
            tweets_file = open('test.json', 'a', encoding='utf-8')
            tweets_file.write(str(tweet))
            tweets_file.close()
        except:
            e = sys.exc_info()[0]
            print( "<p>Error: %s</p>" % e )  
        
    def storeTweetSentiment(self, tweet):
        try:
            related_topic_term = self.isTweetRelatedFF(tweet)[1]
            text = tweet['text']
            sentiment = NaiveBayes.sentimentClassify(text, sentimentTokenizer, stopwords, sentimentClassifier)
            state = getTweetState(tweet)
            
            sentiment_file_writer =  csv.writer(open('FFsentiment.csv','a'), lineterminator='\n')
            sentiment_file_writer.writerow((related_topic_term, tweet['text'], sentiment, state))
        except:
            e = sys.exc_info()[0]
            print( "<p>Error: %s</p>" % e )
    
def getTweetState(tweet):
    west = tweet['place']['bounding_box']['coordinates'][0][0][0]
    east = tweet['place']['bounding_box']['coordinates'][0][2][0]
    north = tweet['place']['bounding_box']['coordinates'][0][2][1]
    south = tweet['place']['bounding_box']['coordinates'][0][0][1]
    
    lat = (north + south)/2
    long = (west+east)/2
    
    #address = geolocator.reverse((lat,long), exactly_one=True)
    location = ''.join([str(lat),",",str(long)])
    state = mapquest(location).state
    return str(state)

def saveCounts():
    with open('total-counts.csv', 'w') as counts:
            counts= csv.DictWriter(counts, states.keys())
            counts.writeheader()
            counts.writerow(states)
    
if __name__ == '__main__':

    #geolocator = GoogleV3()

    tweets = open('test.json', 'w', encoding='utf-8')
    tweets.close()
    
    sentiment_file_writer =  csv.writer(open('FFsentiment.csv','w'), lineterminator='\n')
    
    sentimentClassifier = NaiveBayes.getSentimentClassifier()
    print("Sentiment Classifier Created")
    
    sentimentTokenizer = happytokenizer.TweetTokenizer()

    #This handles Twitter authentication and the connection to Twitter Streaming API
    Tweetlistener = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, Tweetlistener)

    #This line filter Twitter Streams to capture data posted from US in English with utf-8 encoding
    while True:
        try:
            stream.filter(languages=['en'], async=False, locations=[-125,25,-65,48])
        except:
            e = sys.exc_info()[0]
            print("Streaming Error")
            print( "<p>Error: %s</p>" % e )
            saveCounts()
            
    atexit.register(saveCounts)