#DISCLAIMER: this code was run on google colab
import numpy as np
import cv2
import os
from tensorflow.keras.applications import MobileNetV2  # Or MobileNet, ResNet, etc.
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# Path to your UNO card images
data_dir = '/content/Data'

# Load the pre-trained model without the top layers (output layer)
base_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=(224, 224, 3))

# Function to extract features using VGG16
def extract_features(image):
    # Preprocess image for the pre-trained model
    image = cv2.resize(image, (224, 224))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)
    # Get features from the pre-trained model
    features = base_model.predict(image)
    return features.flatten()  # Flatten the 3D features to a 1D array

# Prepare dataset: load images, extract features, and store labels
features = []
labels = []

# Traverse each folder corresponding to each class
for class_name in os.listdir(data_dir):
    class_dir = os.path.join(data_dir, class_name)
    if os.path.isdir(class_dir):
        for image_name in os.listdir(class_dir):
            image_path = os.path.join(class_dir, image_name)
            # Read image
            image = cv2.imread(image_path)
            # Extract features using the pre-trained model
            features.append(extract_features(image))
            labels.append(class_name)

# Convert lists to numpy arrays
features = np.array(features)
labels = np.array(labels)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

from sklearn.svm import SVC

# Initialize and train an SVM classifier
svm = SVC(kernel='linear')  # or 'rbf' for a radial basis function kernel
svm.fit(X_train, y_train)

# Evaluate
y_pred = svm.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy with SVM and Transfer Learning Features: {accuracy * 100:.2f}%")


# #for saving new trained model to google drive
# import joblib

# # Save the trained SVM model to a file
# model_filename = 'svm_uno_model.pkl'
# joblib.dump(svm, model_filename)

# # Optional: Move it to your Google Drive (if you're using Google Colab)
# # from google.colab import drive
# # drive.mount('/content/drive')

# # Move the model to your Google Drive
# !cp svm_uno_model.pkl /content/drive/MyDrive/