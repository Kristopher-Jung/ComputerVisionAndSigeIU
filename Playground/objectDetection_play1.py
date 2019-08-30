import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import glob
import keras
from keras.layers import LeakyReLU, Flatten, Dense
from keras.models import Sequential
from keras.layers.convolutional import Convolution2D, MaxPooling2D

# Pre trained weights require this ordering
keras.backend.set_image_dim_ordering('th')


def get_model():
    model = Sequential()

    # Layer 1
    model.add(Convolution2D(16, 3, 3, input_shape=(3, 448, 448), border_mode='same', subsample=(1, 1)))
    model.add(LeakyReLU(alpha=0.1))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    # Layer 2
    model.add(Convolution2D(32, 3, 3, border_mode='same'))
    model.add(LeakyReLU(alpha=0.1))
    model.add(MaxPooling2D(pool_size=(2, 2), border_mode='valid'))

    # Layer 3
    model.add(Convolution2D(64, 3, 3, border_mode='same'))
    model.add(LeakyReLU(alpha=0.1))
    model.add(MaxPooling2D(pool_size=(2, 2), border_mode='valid'))

    # Layer 4
    model.add(Convolution2D(128, 3, 3, border_mode='same'))
    model.add(LeakyReLU(alpha=0.1))
    model.add(MaxPooling2D(pool_size=(2, 2), border_mode='valid'))

    # Layer 5
    model.add(Convolution2D(256, 3, 3, border_mode='same'))
    model.add(LeakyReLU(alpha=0.1))
    model.add(MaxPooling2D(pool_size=(2, 2), border_mode='valid'))

    # Layer 6
    model.add(Convolution2D(512, 3, 3, border_mode='same'))
    model.add(LeakyReLU(alpha=0.1))
    model.add(MaxPooling2D(pool_size=(2, 2), border_mode='valid'))

    # Layer 7
    model.add(Convolution2D(1024, 3, 3, border_mode='same'))
    model.add(LeakyReLU(alpha=0.1))

    # Layer 8
    model.add(Convolution2D(1024, 3, 3, border_mode='same'))
    model.add(LeakyReLU(alpha=0.1))

    # Layer 9
    model.add(Convolution2D(1024, 3, 3, border_mode='same'))
    model.add(LeakyReLU(alpha=0.1))

    model.add(Flatten())

    # Layer 10
    model.add(Dense(256))

    # Layer 11
    model.add(Dense(4096))
    model.add(LeakyReLU(alpha=0.1))

    # Layer 12
    model.add(Dense(1470))

    return model

def preprocess(fname):
    vidcap = cv2.VideoCapture(fname)
    success, image = vidcap.read()
    count = 0
    while success:
        success, image = vidcap.read()
        image = cv2.resize(image, (448, 448))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("./frames/frame%d.jpg" % count, gray)
        count += 1
        print("count: %d" % count)


if __name__ == '__main__':
    preprocess('5.mp4')
