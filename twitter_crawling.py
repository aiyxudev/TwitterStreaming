import tweepy
import csv
import string
from tweepy import OAuthHandler
from collections import Counter

#Twitter APT credentials
consumer_key = '8Jep0EW9FXECqitumYjHXmIFc'
consumer_secret = 'uyIyaQHGJXccxcfDQ48ojz6wREVM4zTQEpoCQyolpGTxltCONJ'
access_token = '786042255454777345-fywA0wsAROYvVytGbZruR17AutAxpJi'
access_secret = 'H0DsTm3nnxlxdL4AX67CpJT9iwamjyygXN2tBcoQUmoBo'


def get_all_tweets(screen_name):
    '''This method allows us to access and collect data from twitter account.
       The input is the id name of the twitter account we are going to access,
       and the output will be a cvs file that containt most recent 3240 tweets
       from that account.'''

    #authorize twitter, initialize tweepy
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    #initialize a list to hold all the tweepy Tweets
    alltweets = []

    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name, count = 200)

    #save most recent tweets
    alltweets.extend(new_tweets)

    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print('getting tweets before %s' % (oldest))

        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name, count = 200, max_id=oldest)

        #save most recent tweets
        alltweets.extend(new_tweets)

        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print('...%s tweets downloaded so far' %(len(alltweets)))

    #transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode('utf-8')] for tweet in alltweets]

    #write the csv file
    with open('%s_tweets.csv' % screen_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['id','created_at','text'])
        writer.writerows(outtweets)
    pass



def pre_processed(screen_name):
    '''this method allow us to clean up the data we collect. The input is the
       twitter account we are going to access for. And the output will be a list
       of string after pre-processed.'''

    #list a list of strings that count as stopwords 
    stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves',
             'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him',
             'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its',
             'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what',
             'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 
             'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',
             'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 
             'but','if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by',
             'for', 'with', 'about', 'against', 'between', 'into', 'through',
             'during', 'before', 'after', 'above', 'below', 'to', 'from',
             'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
             'further', 'then', 'once', 'here', 'there', 'when', 'where',
             'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
             'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
             'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can',
                 'will', 'just', 'don', 'should', 'now','-']

    #make a list of punctuations
    punct = list(string.punctuation)

    #file operation, access the data in the csv file we made from get_all_tweets()

    #open the files, read only
    infile = open('%s_tweets.csv' % screen_name, 'r')
    #read the files into a list of lines
    lines = infile.readlines()
    #close the file
    infile.close()
    
    #initialize a list to hold words after pre-processed
    filtered_words = []

    #initialize a list to hold words after splitting line
    words = []
    for line in lines:
        words.append(line.lower().split(" "))
    
    #clean up the punctuation and stopwords in the list
    for word in words:
        for item in word:
            #remove the stopwords in the list
            if item not in stopwords:
                #replace the punctuation character in each string with ''
                filtered_words.append(''.join(c for c in item if c not in punct))
    return filtered_words
                
def top_ten(screen_name):
    '''This method print out the top ten frequency words in the list.
    The input is the twitter id we access data from, the output will be
    a dictionary with the words as keys, and frequencies as value'''
 
    #initialized a dict to count the frequency of the word
    my_dict = {}

    #make a list of words which after pre-processed
    filtered = pre_processed(screen_name)

    for word in filtered:
        #if the word didn't appear in the dictionary yet,
        #then add the word into it as a new key
        #and make the value to 1
        if word not in my_dict :
            my_dict[word] = 1
        #if the word already in the dictionary as a key,
        #add 1 to it's value
        else:
            my_dict[word] += 1

    #print out the keys with top ten highest value  
    my_result = dict(Counter(my_dict).most_common(11))#because i can't get rid of *''* in the
    print(my_result)                                  #top ten list, i used top 11 instead.

if __name__ == '__main__':
    '''run the function with @realDonaldTrump twitter account'''
    #pass in the username of the account you want to download
    #get_all_tweets('@scotthutslar')
    #pre_processed('@realDonaldTrump')
    top_ten('@scotthutslar')

##the result of the function
##{'': 354,'people': 194, 'realdonaldtrump': 293, 'trump2016': 148, 'clinton': 212,
## 'amp': 271,'great': 358, 'trump': 269, 'hillary': 328, 'america': 202, 'crooked': 145}
