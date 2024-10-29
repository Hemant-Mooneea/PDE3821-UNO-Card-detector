import cv2
import numpy as np
import joblib
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array

# Load the saved SVM model
model_filename = 'svm_uno_model2.pkl'
svm = joblib.load(model_filename)

# Load the VGG16 model for feature extraction
base_model = VGG16(weights="imagenet", include_top=False, input_shape=(256, 256, 3))

# Function to extract features using VGG16
def extract_features(image):
    image = cv2.resize(image, (256, 256))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)
    features = base_model.predict(image)
    return features.flatten()

# Initialize the webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Extract features from the frame
    features = extract_features(frame)
    features = np.expand_dims(features, axis=0)  # Expand dimensions to match input shape for SVM

    # Predict the class of the card
    prediction = svm.predict(features)
    card_name = prediction[0]  # Get the predicted class name

    # Display the result on the frame
    cv2.putText(frame, card_name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Webcam UNO Card Detection', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
