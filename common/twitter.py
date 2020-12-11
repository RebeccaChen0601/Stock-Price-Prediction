import datetime
import dataclasses
import re

def get_tweet_timestamp(tid):
    if isinstance(tid, str):
        tid = int(tid)
    offset = 1288834974657
    ts = (tid >> 22) + offset
    utcdttime = datetime.datetime.utcfromtimestamp(ts/1000)
    return ts, utcdttime

@dataclasses.dataclass
class ChirpsInstance:
    
    tweetId: str
    pred: str
    predL: str
    arg1: str
    arg2: str
        
    @property
    def timestamp(self):
        return get_tweet_timestamp(self.tweetId)[0]
    @property
    def datetime(self):
        return get_tweet_timestamp(self.tweetId)[1]
    
    @property
    def tokenised_string(self):
        li = self.predL.split(' ')
        
        def submap(x):
            if x == '{a0}':
                return self.arg1
            elif x == '{a1}':
                return self.arg2
            else:
                return x
        li = [submap(x) for x in li]
        return li
    
    @property
    def tokenised_substitute_string(self):
        # Remove punctuations except for {}
        x = re.sub(r'[^\w\s\{\}]','',self.predL)
        x = x.format(a0=self.arg1, a1=self.arg2)
        return x.split(' ')
    
    @property
    def serialise(self):
        return '\t'.join([self.tweetId, self.pred, self.predL, self.arg1, self.arg2])
    
    def __eq__(self, other):
        return self.tweetId == other.tweetId

def chirps_instance_readline(line):
    line = line.strip().split('\t')
    instance1 = ChirpsInstance(tweetId = line[0], pred=line[1], predL=line[2], arg1=line[3], arg2=line[4])
    instance2 = ChirpsInstance(tweetId = line[5], pred=line[6], predL=line[7], arg1=line[8], arg2=line[9])
    return instance1, instance2

def chirps_instance_readhalfline(line):
    # After preprocessing, each line only contains one instance.
    line = line.strip().split('\t')
    instance = ChirpsInstance(tweetId = line[0], pred=line[1], predL=line[2], arg1=line[3], arg2=line[4])
    return instance
