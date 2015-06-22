import os, sys, csv, json, fileinput

#
   
def reduceFeatures(features, stopwords):
    """
    This will remove redundent features of a tweet.
    """
    reducedFeatures=[]
    for feature in features:
        #remove punctuation and single letters
        if len(feature) < 2:
            continue
        #remove series of ...
        elif '..' in feature:
            continue
        #remove anything which is just numbers
        elif feature.isdigit():
            continue
        #remove stop words
        elif feature in stopwords:
            continue
        #remove tags
        elif feature.startswith('@'):
            continue
        #remove URL
        elif feature.startswith('http'):
            continue
        
        reducedFeatures.append(feature)
    
    return reducedFeatures

def tokenize(tweet, tokenizer, stopwords):
    tokens = tokenizer.tokenize(tweet)
    tokens = reduceFeatures(tokens, stopwords)
    return tokens
    #print(tokens)
    
    
    #tweets_file = open(tweets_data_path, "r", encoding='utf-8')
    
    #tweets_data = []
    #for line in tweets_file:
    #     try:
    #        tweet = json.loads(line)
    #        tweets_data.append(tweet)
    #    except:
    #       continue
    
   
    
    #for tweet in tweets_data:
    #    try:
    #        tokenize(tweet['text'])
    #    except:
    #        e = sys.exc_info()[0]
    #        print( "<p>Error: %s</p>" % e )

    #tweets_file.close()