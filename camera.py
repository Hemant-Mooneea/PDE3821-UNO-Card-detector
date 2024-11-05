import cv2
from ultralytics import YOLO

# Load the YOLOv8 model (replace 'trained_model.pt' with your model's path)
model = YOLO('trained_model.pt')

# Start capturing video from the default camera (0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Could not read frame.")
        break
    
    # Perform inference on the current frame
    results = model(frame)
    
    # Render the results on the frame
    frame = results[0].plot()  # Draw bounding boxes on the frame
    
    # Display the frame with detections
    cv2.imshow("YOLOv8 Object Detection", frame)
    
    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
