import cv2
from ultralytics import YOLO

#* loading the YOLOv8 model
model = YOLO('trained_model.pt')

#* loading an image from a file
image_path = 'a.bmp'
frame = cv2.imread(image_path)

#* checking if the image was loaded successfully
if frame is None:
    print("Error: Could not load image.")
    exit()

#* making predictions on the image
results = model(frame)

#* rendering the results on the image and drawing bounding boxes
frame = results[0].plot()

#* displaying the image with detections
cv2.imshow("YOLOv8 Object Detection", frame)

#* waits indefinitely until a key is pressed
cv2.waitKey(0)

#* releases all OpenCV windows
cv2.destroyAllWindows()
