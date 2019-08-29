import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import glob
import keras
from keras.models import Sequential
from keras.layers.convolutional import Convolution2D, MaxPooling2D

def crop_and_resize(image):




if __name__ == '__main__':
    vidcap =cv2.VideoCapture('5.mp4')
    success, image = vidcap.read()
    count=0
    while success:
        success, image = vidcap.read()
        cv2.imwrite("./frames/frame%d.jpg" %count, image)
        count+=1
        print("count: %d" %count)
