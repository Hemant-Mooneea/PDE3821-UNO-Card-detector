from ultralytics import YOLO

if __name__ == '__main__':
    # Load the YOLOv8 model
    model = YOLO('yolov8s.pt')  

    # Train the model
    train_results = model.train(data='data.yaml', epochs=500, patience=30, pretrained=False)  

    # Save the trained model
    model.save('trained_model.pt')

    # Evaluate the model on the validation set
    val_results = model.val(data='data.yaml')  # Evaluate on validation set

    # Evaluate the model on the test set
    test_results = model.val(data='data.yaml', split='test')  # Evaluate on test set


