# UNO Card Classification with YOLOv8 🎴

A custom YOLOv8-based model for accurately classifying and detecting UNO cards in real-time and using file input. This project uses a custom-trained YOLOv8 model to recognize various UNO cards in images, which is needed for the robot playing UNO in the case scenario of the PDE3821 coursework 1.

## Table of Contents
- [Overview](#overview)
- [Dataset](#dataset)
- [Model Architecture](#model-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Results](#results)

## Overview
This project leverages a YOLOv8 model for detecting and classifying UNO cards, trained on a custom dataset of 54 different card types. The primary objective is to recognize individual cards in an image, with efficient processing suitable for real-time applications.

## Dataset
The dataset consists of **1144 images** organized into **3 sets**: a train set, validation set and test set
- **Image Size**: Resized to 640x640 pixels.
- **Annotations**: Bounding boxes around each card to facilitate precise detection.

> Dataset preparation was completed with the help of **YOLO-compatible labeling tools** namely [Label Studio](https://labelstud.io/) and formatted into YOLO’s annotation format.

## Model Architecture
This custom YOLOv8 model configuration has been tailored to efficiently handle the detection and classification of UNO cards. The model uses:

- **Backbone**: Convolutional layers for extracting essential features from images.
- **Head**: Layers for multi-scale detection, enabling accurate card recognition of varying sizes.

The configuration parameters have been optimized to balance detection speed and accuracy, making it effective for real-time use.

## Installation

Clone this repository and install the required dependencies:

```bash
git clone https://github.com/Hemant-Mooneea/PDE3821-UNO-Card-detector.git
cd PDE3821-UNO-Card-detector
pip install -r requirements.txt
```

> **Requirements**: This project relies on Python 3.12, YOLOv8, OpenCV, and other dependencies listed in `requirements.txt`.

## Usage
To run the program, run:

```bash
python main.py
```

This will open a GUI menu with options for detection through webcam or file input.

### Training the Model
To train the model on your dataset, adjust the `data.yaml` file and run:

```bash
python yolo_training.py 
```


