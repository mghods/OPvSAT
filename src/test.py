
import nltk

def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
        all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

if __name__ == '__main__':
    tweets = [
    (['love', 'this', 'car'], 'positive'),
    (['this', 'view', 'amazing'], 'positive'),
    (['feel', 'great', 'this', 'morning'], 'positive'),
    (['excited', 'about', 'the', 'concert'], 'positive'),
    (['best', 'friend'], 'positive'),
    (['not', 'like', 'this', 'car'], 'negative'),
    (['this', 'view', 'horrible'], 'negative'),
    (['feel', 'tired', 'this', 'morning'], 'negative'),
    (['not', 'looking', 'forward', 'the', 'concert'], 'negative'),
    (['enemy'], 'negative')]
    #print(reuters.categories())
    #print(get_words_in_tweets(tweets))
    #word_features = get_word_features(get_words_in_tweets(tweets))