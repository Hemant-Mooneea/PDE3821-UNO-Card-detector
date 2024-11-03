import cv2
import numpy as np
import joblib
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tkinter import *
from tkinter import PhotoImage

#* loading the saved SVM model
modelFilename = 'svm_uno_model4.pkl'
svm = joblib.load(modelFilename)

#* loading the MobileNetV2 model for extracting features
baseModel = MobileNetV2(weights="imagenet", include_top=False, input_shape=(224, 224, 3))

def extractFeatures(image):
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

def classifyCardFromInput(inputField):
    """
    Label card image that has been input
    
    :param inputField: Takes the inputField as parameter in order
    to get the input entered
    """

    #* get path input from input field
    imagePath = inputField.get()

    img = cv2.imread(imagePath)

    if img is None:
        print("Image not found!")
        return

    #* resize the image before it appears
    img = cv2.resize(img, (224, 224))
    #* extracting features from the image
    features = extractFeatures(img)
    #* expanding the dimensions to match the input shape for SVM 
    features = np.expand_dims(features, axis=0)  

    #* predicting the class of the card shown
    prediction = svm.predict(features)
    #* get the predicted class name
    cardName = prediction[0]  

    #* displaying the result on the frame
    cv2.putText(img, cardName, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    #* displatying the resulting frame
    cv2.imshow('Webcam UNO Card Detection', img)

    #? waits for a key press to close window
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#* Function to handle button clicks
def buttonAction(buttonName):
    if buttonName == "Button 1":
        openWindow1()  
    elif buttonName == "Button 2":
        openWindow2()  
    elif buttonName == "Button 3":
        root.quit()  

#* Function to open the Live Camera
def openWindow1():
    """
    Classify card using webcam feed
    
    :return: frame with the card name on it
    """
    #* Hide the main window while showing the camera feed
    root.withdraw()

    #* Initialize the webcam
    cap = cv2.VideoCapture(0)

    while True:
        #* Capture frame by frame
        ret, frame = cap.read()
        if not ret:
            break
        #* extracting features from the frame
        features = extractFeatures(frame)
        #* expanding the dimensions to match the input shape for SVM 
        features = np.expand_dims(features, axis=0)  

        #* predicting the class of the card shown
        prediction = svm.predict(features)
        #* get the predicted class name
        cardName = prediction[0]

        #* Display the resulting frame
        cv2.imshow('Webcam UNO Card Detection', frame)

        #? waits for a key press and if no key is pressed, it allows the program to continue running without pausing
        cv2.waitKey(1)
        
        #? Check if the window is closed by clicking 'X'
        if cv2.getWindowProperty('Webcam UNO Card Detection', cv2.WND_PROP_VISIBLE) < 1:
            break

    #* Release the webcam and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()

    # Show the main Tkinter window again after closing the OpenCV window
    root.deiconify()  

# Function to open the Photo Detection
def openWindow2():
    """
    Classify card from file input
    
    :return: resized image with the card name on it
    """


    root.withdraw()  
    window2 = Toplevel(root)  
    window2.title("Photo Detection")  
    window2.geometry("1000x500")  
    
    
    label = Label(window_2, text="Enter image path: ", font=("Arial", 18))
    label.place(x=400, y=100)

    inputField = Entry(window_2, width=100)
    inputField.place(x=200, y=150)

    submitButton = Button(window_2, text="Submit", command=lambda:classifyCardFromInput(inputField), font=("Arial", 14))
    submitButton.place(x=450, y=180)


    def onClose():
        window2.destroy()  
        root.deiconify()  

    window2.protocol("WM_DELETE_WINDOW", onClose)  
    closeButton = Button(window2, text="Close", command=onClose, font=("Arial", 14))
    closeButton.place(x=900, y=10)

# Create the main window
root = Tk()
root.title("UNO Card Detection")
root.geometry("1000x550+300+200")
root.configure(bg="#fff")
root.resizable(True, True)

# Load image for the main window
try:
    img = PhotoImage(file="uno.png")
    imageLabel = Label(root, image=img, bg='white')
    imageLabel.place(x=30, y=25)
except Exception as e:
    print("Error loading image:", e)

# Main menu layout
frame = Frame(root, bg="white")
frame.place(x=500, y=70, width=400, height=350)  

heading = Label(frame, text='Welcome', fg='#57a1f8', bg='white',
                font=("Times", "50", "bold italic"))
heading.place(x=100, y=5)

subheading = Label(frame, text='UNO Detection Card', fg='black', bg='white',
                   font=("Verdana", "15", "italic"))  
subheading.place(x=130, y=75)  

# Create buttons in the main window
button1 = Button(frame, text="Open Camera", command=lambda: buttonAction("Button 1"), 
                 bg="#57a1f8", fg="white", font=("Arial", 14), relief="flat")
button1.place(x=100, y=170, width=300, height=40)

button2 = Button(frame, text="Photo Detection", command=lambda: buttonAction("Button 2"), 
                 bg="#57a1f8", fg="white", font=("Arial", 14), relief="flat")
button2.place(x=100, y=240, width=300, height=40)

button3 = Button(frame, text="Exit", command=lambda: buttonAction("Button 3"), 
                 bg="#57a1f8", fg="white", font=("Arial", 14), relief="flat")
button3.place(x=100, y=310, width=300, height=40)

root.mainloop()

