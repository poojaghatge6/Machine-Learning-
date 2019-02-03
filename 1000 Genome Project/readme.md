Aim: To predict a person's geographic position from its genotype.

Data Source:
https://storage.googleapis.com/kmeans_data/large_train [6 GB]
https://storage.googleapis.com/kmeans_data/train_labels

-Implemented kNN(k-nearest neighbors) algorithm in a distributed environment of Google Cloud DataProc on a cluster with 16 quad-core worker nodes which gave 92.2% accuracy within 15mins.

-The dataset was loaded as Resilient Distributed Datasets(Rdd) and various Rdd operations like MapReduce, broadcast, collect, etc., were performed on it.

Technology Stack: Google Cloud DataProc cluster, pyspark, python.


Execution:
```linux
gcloud dataproc clusters create kmeans-pooja --zone us-east1-b --region us-east1 --num-workers 16 --properties spark:spark.executor.heartbeatInterval=120,spark:spark.dynamicAllocation.enabled=false --initialization-actions gs://kmeans_data/dataproc.init
gcloud dataproc jobs submit pyspark 1000Genome.py --cluster kmeans-pooja --region us-east1 -- gs://kmeans_data/train_labels gs://kmeans_data/large_train gs://kmeans_data/large_test predictions

```
