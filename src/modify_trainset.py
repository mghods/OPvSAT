import os, sys, csv, random
import happytokenizer

# current workspace os path
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

tokenizer = happytokenizer.TweetTokenizer()
stopwords_path = os.path.join(__location__, 'stopwords.csv')
stopsowrds_file = open(stopwords_path, newline='')
stopwords = list(csv.reader(stopsowrds_file, delimiter=','))[0]

def tokenize(tweet):
    tokens = tokenizer.tokenize(tweet)
    tokens = reduceFeatures(tokens)
    return tokens

def reduceFeatures(features):
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

def randomeTrainSet():
    trainset_path = os.path.join(__location__, '140SA_training.csv')
    modifiedtrainset_path = os.path.join(__location__, '140SA_training_Random.csv')
    trainset_file_reader = csv.reader(open(trainset_path, 'r'))
    trainset_file_writer =  csv.writer(open(modifiedtrainset_path,'w'), lineterminator='\n')
    data = list(trainset_file_reader)
    for x in range(0,10000):
        trainset_file_writer.writerow( data[random.randint(0,1600000)] )
    
    
def modifyTrainSet():
    #modifying train set
    #for the purpose of training we have used 140 sentiment set downloaded from:
    # http://cs.stanford.edu/people/alecmgo/trainingandtestdata.zip 
    trainset_path = os.path.join(__location__, '140SA_training_Random.csv')
    modifiedtrainset_path = os.path.join(__location__, '140SA_training_modified.csv')
    trainset_file_reader = csv.reader(open(trainset_path, 'r'))
    trainset_file_writer =  csv.writer(open(modifiedtrainset_path,'w'), lineterminator='\n')
    
    # Only keep column 0 (sentiment polarity) and column 5 (tweets) 
    # while converting column 0 values from [0,2,4] to [-1,0,1] for negative, neutral, and positive respectivly
    
    for row in trainset_file_reader:
        trainset_file_writer.writerow((int((int(row[0])-2)/2),' '.join(tokenize(row[5]))))
    
if __name__ == '__main__':
    randomeTrainSet()
    modifyTrainSet()
    