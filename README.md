# UNO Card Classification with YOLOv8 🎴

A custom YOLOv8-based model for accurately classifying and detecting UNO cards in real-time and using file input. This project uses a custom-trained YOLOv8 model to recognize various UNO cards in images, which is needed for the robot playing UNO in the case scenario of the PDE3821 coursework 1.

## Table of Contents
- [Overview](#overview)
- [Dataset](#dataset)
- [Model Architecture](#model-architecture)
- [Installation](#installation)
- [Usage](#usage)

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
**PyTorch Installation (for GPU Inference)**

To enable GPU inference for faster processing, you’ll need to install PyTorch with CUDA support. Follow these steps

1. **Check CUDA Availability**: Ensure your system has an NVIDIA GPU that supports CUDA.

2. **Install PyTorch with CUDA**:
   Visit the [PyTorch installation page](https://pytorch.org/get-started/locally/) 

**Image Augmentation during training**

To have the augmentation during training similar to what was done for this model do the following
1. Navigate to the folder/virtual environment where the python libraries are installed
2. Navigated to the "Lib" folder 
3. Inside of the "site-packages" folder look for another folder called "ultralytics"
4. Inside of "ultralytics" find the "cfg" folder
5. Inside the "cfg" folder look for "default.yaml" and scroll downwards 
6. Finally replace the hyperparameters with the ones below

```
# Hyperparameters ------------------------------------------------------------------------------------------------------
lr0: 0.01 # (float) initial learning rate (i.e. SGD=1E-2, Adam=1E-3)
lrf: 0.01 # (float) final learning rate (lr0 * lrf)
momentum: 0.937 # (float) SGD momentum/Adam beta1
weight_decay: 0.0005 # (float) optimizer weight decay 5e-4
warmup_epochs: 3.0 # (float) warmup epochs (fractions ok)
warmup_momentum: 0.8 # (float) warmup initial momentum
warmup_bias_lr: 0.1 # (float) warmup initial bias lr
box: 7.5 # (float) box loss gain
cls: 0.5 # (float) cls loss gain (scale with pixels)
dfl: 1.5 # (float) dfl loss gain
pose: 12.0 # (float) pose loss gain
kobj: 1.0 # (float) keypoint obj loss gain
label_smoothing: 0.0 # (float) label smoothing (fraction)
nbs: 64 # (int) nominal batch size
hsv_h: 0.025 # (float) image HSV-Hue augmentation (fraction)
hsv_s: 0.3 # (float) image HSV-Saturation augmentation (fraction)
hsv_v: 0.5 # (float) image HSV-Value augmentation (fraction)
degrees: 15.0 # (float) image rotation (+/- deg)
translate: 0.2 # (float) image translation (+/- fraction)
scale: 0.5 # (float) image scale (+/- gain)
shear: 0.0 # (float) image shear (+/- deg)
perspective: 0.0 # (float) image perspective (+/- fraction), range 0-0.001
flipud: 0.0 # (float) image flip up-down (probability)
fliplr: 0.0 # (float) image flip left-right (probability)
bgr: 0.0 # (float) image channel BGR (probability)
mosaic: 0.8 # (float) image mosaic (probability)
mixup: 0.0 # (float) image mixup (probability)
copy_paste: 0.0 # (float) segment copy-paste (probability)
copy_paste_mode: "flip" # (str) the method to do copy_paste augmentation (flip, mixup)
auto_augment: randaugment # (str) auto augmentation policy for classification (randaugment, autoaugment, augmix)
erasing: 0.4
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


