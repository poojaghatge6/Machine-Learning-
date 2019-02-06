import pyspark
import sys
import os
import numpy as np
from pyspark.sql.types import IntegerType
from pyspark.sql import SparkSession
from pyspark.sql.types import FloatType
from pyspark.sql.functions import mean
from pyspark.sql.functions import broadcast
from pyspark.ml.recommendation import ALS

def split_map(row):
    p=row.value.split(" ")
    return  (int(p[0]),(int(p[1]),float(p[2])))

def mini(x,y):
    if(x[1]>y[1]):
        return x
    else:
        return y

spark = pyspark.sql.SparkSession.builder.getOrCreate()
sc=spark.sparkContext
sim_targets=spark.read.text("gs://mscbio2065-data/targ_sim.txt").rdd
sim_compounds=spark.read.text("gs://mscbio2065-data/correct_cmpd_sim.txt").rdd
df_train = spark.read.csv(sys.argv[1])
df_missing = spark.read.csv(sys.argv[2])
out = open(sys.argv[3],'w')

df_train = df_train.withColumn("_c0", df_train["_c0"].cast(IntegerType()))
df_train = df_train.withColumn("_c1", df_train["_c1"].cast(IntegerType()))
df_train = df_train.withColumn("_c2", df_train["_c2"].cast(FloatType()))
df_missing = df_missing.withColumn("_c0", df_missing["_c0"].cast(IntegerType()))
df_missing = df_missing.withColumn("_c1", df_missing["_c1"].cast(IntegerType()))
df_missing = df_missing.na.fill(0)

missing_target=set(df_missing.select('_c1').rdd.map(lambda r : r[0]).collect())
train_target=set(df_train.select('_c1').rdd.map(lambda r : r[0]).collect())
missing_target_few=missing_target-train_target
missing_target_few_b=sc.broadcast(missing_target_few)
target_sim_RDD = sim_targets.map(split_map).filter(lambda p: (p[0] in missing_target_few_b.value))
train_target=sc.broadcast(train_target)
target_sim_RDD = target_sim_RDD.filter(lambda p: (p[1][0] in train_target.value))
tmp1=target_sim_RDD.reduceByKey(mini).map(lambda p: (p[0],p[1][0])).collectAsMap()

avgTrain_target=dict()
avgTrain_target=df_train.rdd.map(lambda x: (x[1],x[2])).reduceByKey(lambda x,y: (x+y)/2.0).collectAsMap()
avgMissing_target=dict()    
for i in missing_target:
    if(i in missing_target_few): average=avgTrain_target[tmp1[i]]
    else: average=avgTrain_target[i]
    avgMissing_target[i]=average

missing_cmpd=set(df_missing.select('_c0').rdd.map(lambda r : r[0]).collect())
train_cmpd=set(df_train.select('_c0').rdd.map(lambda r : r[0]).collect())
missing_cmpd_few=missing_cmpd-train_cmpd
missing_cmpd_few_b=sc.broadcast(missing_cmpd_few)
compound_sim_RDD = sim_compounds.map(split_map).filter(lambda p: (p[0] in missing_cmpd_few_b.value))
train_cmpd=sc.broadcast(train_cmpd)
compound_sim_RDD = compound_sim_RDD.filter(lambda p: (p[1][0] in train_cmpd.value))
tmp2=compound_sim_RDD.reduceByKey(mini).map(lambda p: (p[0],p[1][0])).collectAsMap()

avgTrain_cmpd=dict()
avgTrain_cmpd=df_train.rdd.map(lambda x: (x[0],x[2])).reduceByKey(lambda x,y: (x+y)/2.0).collectAsMap()
avgMissing_cmpd=dict()
for i in missing_cmpd:
    if(i in missing_cmpd_few): average=avgTrain_cmpd[tmp2[i]]
    else: average=avgTrain_cmpd[i]
    avgMissing_cmpd[i]=average

avg_compound=sc.broadcast(avgMissing_cmpd)
avg_target=sc.broadcast(avgMissing_target)
filled_missing=df_missing.rdd.map(lambda x: (x[0],x[1],((avg_compound.value[x[0]]+avg_target.value[x[1]])/2.0))).collect()
filled_missing=spark.createDataFrame(filled_missing)
df_train=df_train.union(filled_missing)

als=ALS(rank=15, maxIter=15, regParam=2,userCol="_c0", itemCol="_c1", ratingCol="_c2",nonnegative=True)
model = als.fit(df_train)
predictions= model.transform(df_missing)
predictions=predictions.collect()

for i in predictions:
    out.write('%s,%s,%s\n' % (str(i[0]),str(i[1]),str(i[2])))
out.close()
