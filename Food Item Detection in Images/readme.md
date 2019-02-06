Team members: Pooja Ghatge, Brandan Dunham

Research advisor: Dr. Madhavi Ganapathiraju (Department of Biomedical Informatics)

Techniques: Object Detection in images, Active Learning, Deep Learning(Artificial Neural Networks).
Technology: Tensorflow, Google Cloud, Python.
Data Size:
1) 86 GB (training images)
2) 12 GB (test images)
3) 4 GB (validation images)
Data Source: https://storage.googleapis.com/openimages/web/download.html
Background(Project Scope): The idea of the project is to be able to train a neural network that can identify the individual constituent food items from images of meals that a user uploads. We focus on identifying 80 different food items for this project as the available data is limited to it. The data contains images as its data for training the network, and bounding boxes of food as instances, with their names as class labels. Google Open Images contain object-recognized images (550GB) pertaining to different objects out of which we choose 86GB of food item tagged/labeled data.

Innovation: We are going to set aside a certain percentage of training data to simulate an active learning model and test the performance with and without active learning.

Outcome: Identified food items in images. Faster, less extensive training with active learning than regular training while still getting good results.
