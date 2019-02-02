Aim: To predict a person's geographic position from its genotype.

Data Source: https://storage.googleapis.com/kmeans_data/large_train [6 GB]

-Implemented kNN in a distributed environment of Google Cloud DataProc on a cluster with 16 worker nodes.
-The dataset was loaded as Resilient Distributed Datasets(Rdd) and various Rdd operations like MapReduce, broadcast, collect, etc., were performed on it.

Technology Stack: Google Cloud DataProc cluster, pyspark, python.
