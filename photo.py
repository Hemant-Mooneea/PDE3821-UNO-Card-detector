import cv2
from ultralytics import YOLO

# Load the YOLOv8 model (replace 'trained_model.pt' with your model's path)
model = YOLO('trained_model.pt')

# Load an image from a file (replace 'image.jpg' with your image file path)
image_path = 'a.bmp'  # Change this to your image file
frame = cv2.imread(image_path)

# Check if the image was loaded successfully
if frame is None:
    print("Error: Could not load image.")
    exit()

# Perform inference on the image
results = model(frame)

# Render the results on the image
frame = results[0].plot()  # Draw bounding boxes on the image

# Display the image with detections
cv2.imshow("YOLOv8 Object Detection", frame)

# Wait indefinitely until a key is pressed
cv2.waitKey(0)

# Release all OpenCV windows
cv2.destroyAllWindows()
