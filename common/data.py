import datetime
import numpy as N
import numpy.random as NR
import common.twitter

def create_tweets_rdd(path, sc, partitions=80):
    """
    Read [(date, string)] rdd from tokenised tweets.
    """
    
    def read_tweet(x):
        x = common.twitter.chirps_instance_readhalfline(x)
        _,timestamp = common.twitter.get_tweet_timestamp(x.tweetId)
        return timestamp.date(), ' '.join(x.tokenised_substitute_string)
    
    return sc.textFile(str(path), partitions) \
        .map(read_tweet)

def create_data_rdd(samplesRdd, datesIdx, sc,
                    windowSize=7, leadTime=None, partitions=30, sampleSize=1000, nSamplesPerDay=30):
    """
    Create a [(date, [sample])] RDD for caching
    """
    if leadTime is None:
        leadTime = windowSize
        
    startDay = datesIdx.min() + datetime.timedelta(leadTime)
    
    mask = datesIdx.map(lambda x:x >= startDay)
    #seriesRdd = sc.paralellize(zip(series.index, series), partitions)
    
    b_idxMask = sc.broadcast(set(datesIdx[mask]))
    
    def sample_duplication_func(args):
        date, x = args
        result = [(date+datetime.timedelta(i), x) for i in range(0,windowSize+1)]
        result = [(x,[y]) for x,y in result if x in b_idxMask.value]
        return result
    
    def safechoice(li, sampleSize):
        if len(li) > sampleSize:
            return NR.choice(li, sampleSize, replace=False)
        else:
            return NR.choice(li, sampleSize, replace=True)
            
    
    def date_sample_func(args):
        date, li = args
        NR.seed((date - startDay).days)
        return [(date, safechoice(li, sampleSize))
                for _ in range(nSamplesPerDay)]
    
    
    # Duplicate each sample
    samplesRdd = (samplesRdd
        .flatMap(sample_duplication_func)
        .reduceByKey(lambda a,b:a+b, numPartitions=partitions)
        .flatMap(date_sample_func)
        )
    return samplesRdd


        
def get_data_to_sample_transform(word2vec, embeddingProperties, series, sc):
    """
    Take a [(date, [tweets])] RDD and output [(embedded tweets, Y)] RDD.
    """
    b_word2vec = sc.broadcast(word2vec)
    
    def embed_tweet(li):
        zero = N.zeros(embeddingProperties['embedding_size'])
        li = [b_word2vec.value.get(x, zero) for x in li]
        dl = embeddingProperties['tweet_len'] - len(li)
        assert dl >= 0
        li = N.stack(li)
        # Pad result so they all have 26 words.
        return N.pad(li, ((0, dl), (0,0)))
    
    def sample_transform_func(args):
        date, listTweets = args
        listTweets = N.stack([embed_tweet(x.split(' ')) for x in listTweets])
        return listTweets, series[date]
    
    return sample_transform_func