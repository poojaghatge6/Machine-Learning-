Aim: To predict a person's geographic position from its genotype.

Introduction:
We are just 0.1% different from other individuals based on our genome. Human Genomes are 99.9% similar to each other. When we study this 0.1% genomic variations, we can draw interesting conclusions like their geographic locations, diseases, etc.

Data Source and Description:
- https://storage.googleapis.com/kmeans_data/large_train [6 GB]
  * This file contains person's id, position on the genome of the variant, and number of the variants 0, 1 or 2 at that position for that individual. It describes the variants in different individuals.
```
NA21141 15273 2
NA21144 15273 2
HG00096 57322 0
HG00099 57322 0
```
- https://storage.googleapis.com/kmeans_data/train_labels
  * The mapping of people's id with their geographic location.
```
NA20763 EUR
HG01589 SAS
HG03488 SAS
HG02155 EAS
HG03754 SAS
HG03571 AFR
```

Highlights:
- Google Cloud Dataproc provides Spark and Hadoop clusters used for big data and distributed computing.
- Implemented kNN(k-nearest neighbors) algorithm in a distributed environment on a Spark cluster with 16 quad-core worker nodes which gave 92.2% accuracy within 15mins.
- The dataset was loaded as Resilient Distributed Datasets(Rdd) and various operations like MapReduce, broadcast, collect, filter etc., were performed on the Rdd.
- The neighbors are decided based on the distance between their genetic fingerprint.
- The speciality of using Spark Rdd is that although data appears as a single unit, it is distributed and stored in the Main Memory of the various worker nodes which increases the computational speed.

Technology Stack: Google Cloud SDK, Google Cloud Dataproc, Spark, pyspark, python.

Important steps:

- Download Google Cloud SDK and login using your google account credentials to continue with the next steps on its console.
- Select a project associated with your billing account.
- Run the execution steps shown below with your own cluster name, resources and location preferences.
- It is better if you have your storage bucket and cluster in the same region.
- Dont't forget to delete the cluster once you finish the execution otherwise, money will be deducted from your billing account for using the resources.


Execution:
```linux
gcloud dataproc clusters create cluster_name --zone us-east1-b --region us-east1 --num-workers 16 --properties spark:spark.executor.heartbeatInterval=120,spark:spark.dynamicAllocation.enabled=false --initialization-actions gs://kmeans_data/dataproc.init
gcloud dataproc jobs submit pyspark 1000Genome.py --cluster cluster_name --region us-east1 -- gs://kmeans_data/train_labels gs://kmeans_data/large_train gs://kmeans_data/large_test predictions
gcloud dataproc clusters delete cluster_name --region us-east1 --quiet

```
