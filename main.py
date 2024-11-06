import cv2
from ultralytics import YOLO
from tkinter import *
from tkinter import PhotoImage

#* loading the YOLOv8 model
model = YOLO('trained_model.pt')


def buttonAction(buttonName):
    """
    Switch windows according to button pressed
    
    :param button_name: Takes the button name and depending on it
    switch to the corresponding window
    """
    if buttonName == "Button 1":
        openWindow1()  
    elif buttonName == "Button 2":
        openWindow2()  
    elif buttonName == "Button 3":
        root.quit()  

def classifyCardFromInput(inputField):
    """
    Classify card image that has been input
    
    :param inputField: Takes the inputField as parameter in order
    to get the input entered
    """

    #* get path input from input field
    imagePath = inputField.get()

    img = cv2.imread(imagePath)

    if img is None:
        print("Image not found!")
        return

    #* making predictions on image
    results = model(img)

    #* rendering the results on the image and drawing bounding boxes
    img = results[0].plot()

    #* displaying the image with detections
    cv2.imshow("YOLOv8 Object Detection", img)

    #* waiting indefinitely until a key is pressed
    cv2.waitKey(0)

    #* release all OpenCV windows
    cv2.destroyAllWindows()

def openWindow1():
    """
    Classify card using webcam feed
    
    :return: frame with the card name on it
    """
    #* starts capturing video from the default camera (0)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()

    while True:
        #* reads a frame from the camera
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Could not read frame.")
            break
        
        #* making predictions on the current frame
        results = model(frame)
        
        #* rendering the results on the frame and drawing bounding boxes
        frame = results[0].plot()
        
        #* displaying the frame with detections
        cv2.imshow("YOLOv8 Object Detection", frame)

        #? waits for a key press, and if no key is pressed, it allows the program to continue running without pausing
        cv2.waitKey(1)
        
        #? Check if the window is closed by clicking 'X'
        if cv2.getWindowProperty('YOLOv8 Object Detection', cv2.WND_PROP_VISIBLE) < 1:
            break

    #* releasing the video capture object and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()


def openWindow2():
    """
    Classify card from file input
    
    :return: resized image with the card name on it
    """

    #* hiding the main window
    root.withdraw()  
    window_2 = Toplevel(root)  
    window_2.title("Photo Detection")  
    window_2.geometry("1000x500")  

    label = Label(window_2, text="Enter image path: ", font=("Arial", 18))
    label.place(x=400, y=100)

    inputField = Entry(window_2, width=100)
    inputField.place(x=200, y=150)

    submitButton = Button(window_2, text="Submit", command=lambda:classifyCardFromInput(inputField), font=("Arial", 14))
    submitButton.place(x=450, y=180)

    def on_close():
        #* closes the new window
        window_2.destroy()  
        root.deiconify() 

    close_button = Button(window_2, text="Close", command=on_close, font=("Arial", 14))
    close_button.place(x=900, y=10)  


#* creates the main window
root = Tk()
root.title("UNO Card Detection")

root.geometry("1000x550+300+200")
root.configure(bg="#fff")

#* makes the window resizable
root.resizable(True, True)

img = PhotoImage(file="uno.png")
image_label = Label(root, image=img, bg='white')
image_label.place(x=30, y=25)  
frame = Frame(root, bg="white")
frame.place(x=500, y=70, width=400, height=350)  

heading = Label(frame, text='Welcome', fg='#57a1f8', bg='white',
                font=("Times", "50", "bold italic"))
heading.place(x=100, y=5)

subheading = Label(frame, text='UNO Detection Card', fg='black', bg='white',
                   font=("Verdana", "15", "italic"))  
subheading.place(x=130, y=75)  

#* creates the menu buttons
button1 = Button(frame, text="Open Camera", command=lambda: buttonAction("Button 1"), 
                 bg="#57a1f8", fg="white", font=("Arial", 14), relief="flat")
button1.place(x=100, y=170, width=300, height=40)

button2 = Button(frame, text="Photo Detection", command=lambda: buttonAction("Button 2"), 
                 bg="#57a1f8", fg="white", font=("Arial", 14), relief="flat")
button2.place(x=100, y=240, width=300, height=40)

button3 = Button(frame, text="Exit", command=lambda: buttonAction("Button 3"), 
                 bg="#57a1f8", fg="white", font=("Arial", 14), relief="flat")
button3.place(x=100, y=310, width=300, height=40)

#* binds the close event (when clicking the "X" button)
root.protocol("WM_DELETE_WINDOW", lambda: root.destroy())

root.mainloop()
