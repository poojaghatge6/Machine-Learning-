import os,sys
import pyspark
from collections import Counter
# import time
if len(sys.argv) != 5:
    sys.stderr.write("Need training labels, training data, test data, and output file name\n")
    sys.exit(1)
n=64
sc = pyspark.SparkContext.getOrCreate()
# start=time.time()
data_train=sc.textFile(sys.argv[2],minPartitions=n).distinct()
data_test=sc.textFile(sys.argv[3],minPartitions=n).distinct()

def key_value(s):
    words=s.rstrip().split()
    value=(int(words[1]),int(words[2]))
    key=words[0]
    return (key,value)

def trainKey_distance(x):
    matches=set(p.value[1]).intersection(x[1])
    matches_count=len(matches)
    return (matches_count,[x[0]])

def red_key(s1,s2):
    return s1+s2

lfile = sys.argv[1]
labels = dict()
for line in sc.textFile(lfile).collect():
    (name,val) = line.rstrip().split()
    labels[name] = val
    
data_train=data_train.map(key_value).filter(lambda x: x[1][1] != 0).reduceByKey(red_key)
data_test=data_test.map(key_value).filter(lambda x: x[1][1] != 0).reduceByKey(red_key).collect()

k=15
out = open(sys.argv[4],'w')
# ct=0

for i in data_test:
    p=sc.broadcast(i)
#     ct=ct+1
    vector_k=data_train.map(lambda x: trainKey_distance(x)).reduceByKey(red_key).top(k)
    cnt=Counter()
    for j in vector_k:
        for m in j[1]:
            cnt[labels[m]]+=1
        if(len(j[1])>5): break
    place,count= cnt.most_common(1)[0]
    out.write('%s %s\n' % (i[0],place))
#     end=time.time()
#     print('%s %s\n' % (ct,end-start))
out.close()