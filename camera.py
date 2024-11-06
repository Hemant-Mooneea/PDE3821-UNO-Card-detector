import cv2
from ultralytics import YOLO

#* loading the YOLOv8 model
model = YOLO('trained_model.pt')

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

#* releases the video capture object and closes all OpenCV windows
cap.release()
cv2.destroyAllWindows()
