import cv2
import numpy as np
import joblib
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array

#* loading the saved SVM model
modelFilename = 'svm_uno_model3.pkl'
svm = joblib.load(modelFilename)

#* loading the MobileNetV2 model for extracting features
baseModel = MobileNetV2(weights="imagenet", include_top=False, input_shape=(224, 224, 3))

def extract_features(image):
    """
    Extract features using the MobileNetV2 model

    :param image: Takes an image as parameter, in this case, it is 
    a frame of the live feed where the card appears
    :return: returns a 1 dimensional list/array of the features identified
    """
    image = cv2.resize(image, (224, 224))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)
    features = baseModel.predict(image)
    return features.flatten()


def classifyCard(imagePath):

    img = cv2.imread(imagePath)

    if img is None:
        print("Image not found!")
        return

    #* extracting features from the image
    features = extract_features(img)
    #* expanding the dimensions to match the input shape for SVM 
    features = np.expand_dims(features, axis=0)  

    #* predicting the class of the card shown
    prediction = svm.predict(features)
    #* get the predicted class name
    cardName = prediction[0]  

    #* displaying the result on the frame
    cv2.putText(img, cardName, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    #* displatying the resulting frame
    cv2.imshow('Webcam UNO Card Detection', img)

    #? waits for a key press to close window
    cv2.waitKey(0)
    cv2.destroyAllWindows()

