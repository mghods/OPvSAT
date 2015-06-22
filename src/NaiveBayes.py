import os, csv
import nltk
import happytokenizer, BDTokenizer

# current workspace os path
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


tokenizer = happytokenizer.TweetTokenizer()
stopwords_path = os.path.join(__location__, 'stopwords.csv')
stopsowrds_file = open(stopwords_path, newline='')
stopwords = list(csv.reader(stopsowrds_file, delimiter=','))[0]

word_features=[]
training_tweets=[]

def get_words_in_tweets():
    modifiedtrainset_path = os.path.join(__location__, '140SA_training_modified.csv')
    modifiedtrainset_reader = csv.reader(open(modifiedtrainset_path, 'r'))
    all_words = []
    for row in modifiedtrainset_reader:
        all_words.extend(row[1].split())
    return all_words

def get_word_features(wordlist):
    global word_features
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

def train_extract_features(tweet):
    global word_features
    document_words = set(tweet)
    #print(document_words)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

def extract_features(tweet, tokenizer, stopwords):
    global word_features
    document_words = BDTokenizer.tokenize(tweet, tokenizer, stopwords)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features


def document_tweets(tweet):
    if int(tweet[0]) == -1:
        sentiment = 'negative'
    elif int(tweet[0]) == 0:
        sentiment = 'neutral'
    elif int(tweet[0]) == 1:
        sentiment = 'positive'
    
    #print((tweet[1].split(), sentiment))
    return (tweet[1].split(), sentiment)
    
def getSentimentClassifier():
    get_word_features(get_words_in_tweets())
    modifiedtrainset_path = os.path.join(__location__, '140SA_training_modified.csv')
    modifiedtrainset_reader = csv.reader(open(modifiedtrainset_path, 'r'))
    for row in modifiedtrainset_reader:
        training_tweets.append(document_tweets(row))
    training_set = nltk.classify.apply_features(train_extract_features, training_tweets)
    classifier = nltk.NaiveBayesClassifier.train(training_set)
    return classifier

def sentimentClassify(tweet, tokenizer, stopwords, classifier):
    sentiment = classifier.classify(extract_features(tweet, tokenizer, stopwords))
    return sentiment


