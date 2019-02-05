Aim: To predict a person's geographic position from its genotype.

Data Source:
https://storage.googleapis.com/kmeans_data/large_train [6 GB]
https://storage.googleapis.com/kmeans_data/train_labels

-Google Cloud Dataproc provides Spark and Hadoop clusters used for big data and distributed computing.

-Implemented kNN(k-nearest neighbors) algorithm in a distributed environment on a Spark cluster with 16 quad-core worker nodes which gave 92.2% accuracy within 15mins.

-The dataset was loaded as Resilient Distributed Datasets(Rdd) and various operations like MapReduce, broadcast, collect, filter etc., were performed on the Rdd.

-The speciality of using Rdd is that it keeps the data in the Main Memory of the various worker nodes.

Technology Stack: Google Cloud SDK, Google Cloud Dataproc, Spark, pyspark, python.

Important steps:

-Download Google Cloud SDK and login using your google account credentials to continue with the next steps on its console.

-Select a project associated with your billing account.

-Run the execution steps shown below with your own cluster name, resources and location preferences.

-It is better if you have your storage bucket and cluster in the same region.

-Dont't forget to delete the cluster once you finish the execution otherwise, money will be deducted from your billing account for using the resources.


Execution:
```linux
gcloud dataproc clusters create kmeans-pooja --zone us-east1-b --region us-east1 --num-workers 16 --properties spark:spark.executor.heartbeatInterval=120,spark:spark.dynamicAllocation.enabled=false --initialization-actions gs://kmeans_data/dataproc.init
gcloud dataproc jobs submit pyspark 1000Genome.py --cluster kmeans-pooja --region us-east1 -- gs://kmeans_data/train_labels gs://kmeans_data/large_train gs://kmeans_data/large_test predictions

```
