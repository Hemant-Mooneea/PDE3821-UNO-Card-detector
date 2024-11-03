
#! DISCLAIMER: code to be on google colab preferrably
import numpy as np
import cv2
import os
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# setting the path to the directory containing the Uno card images
dataDirectory = '/content/Data'

# loading the MobileNetV2 base model to extract features from the images
# include_top is set to False so that only the features are returned and not the final classes
baseModel = MobileNetV2(weights="imagenet", include_top=False, input_shape=(224, 224, 3))

def extractFeatures(image):
    """
    Takes an image as parameter and extracts features from it using the pre trained model
    param:image: image to extract features from
    return: features: 1D array of the extracted features
    """
    # preprocessing the image for the pre trained model
    image = cv2.resize(image, (224, 224))
    image = img_to_array(image)
    #adds a new dimension so MobileNetV2 gets input in the expected format
    image = np.expand_dims(image, axis=0)
    #adds pixel values to match MobileNetV2's expectations
    image = preprocess_input(image)

    # obtain features from the pre-trained model
    features = baseModel.predict(image)

    # converts 3D features to a 1D array to make them compatible with standard machine learning models
    return features.flatten()  

# create lists to store features and labels for each image
features = []
labels = []

# goes through each folder corresponding to each class
for className in os.listdir(dataDirectory):
    classDirectory = os.path.join(dataDirectory, className)
    #ensures only folders are processed
    if os.path.isdir(classDirectory):
        for imageName in os.listdir(classDirectory):
            imagePath = os.path.join(classDirectory, imageName)
            # reads the image
            image = cv2.imread(imagePath)
            # extracts features from the image and add them to features list
            features.append(extractFeatures(image))
            #adds the class name to the labels list
            labels.append(className)

# converting lists to numpy arrays to make them easier to use for machine learning
features = np.array(features)
labels = np.array(labels)


# splits the data into training and testing sets
# sets 20% for testing and the remaining 80% is left for training
#random_state = 42 ensures that the split can be reproduced every time with the same random seed
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)


# Support Vector Classifier (SVC) is imported for classification
from sklearn.svm import SVC

# initializes an SVM classifier with a linear kernel
svm = SVC(kernel='linear')

#trains SVM on training data X_train and labels y_train
svm.fit(X_train, y_train)

# uses the trained SVM model to predict labels for the X_test
y_pred = svm.predict(X_test)

#calculates accuracy of the model's predictions by comparing y_test(actual labels) with y_pred(predicted labels)
accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy with SVM and Transfer Learning Features: {accuracy * 100:.2f}%")
