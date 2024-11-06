from ultralytics import YOLO

if __name__ == '__main__':
    #*loading the YOLOv8 model
    model = YOLO('customyolo.yaml')  

    #* training the model
    #? if there is no improvement in 30 epochs (training rounds), model automatically stops training
    #? setting pretrained = False so that model does not use any previously learned patterns, 
    #? it will basically learn everything from scratch based only on our dataset (data.yaml)
    train_results = model.train(data='data.yaml', epochs=500, patience=30, pretrained=False)  

    #*saving the trained model
    model.save('trained_model.pt')

    #* evaluating the model on the validation set
    val_results = model.val(data='data.yaml') 

    #* evaluating the model on the test set
    test_results = model.val(data='data.yaml', split='test')


