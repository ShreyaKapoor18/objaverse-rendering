import numpy as np # linear algebra
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import os
import time
from os.path import join, dirname
from PIL import Image
import objaverse
import cv2
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Flatten, Conv2D, MaxPooling2D
from keras.layers import BatchNormalization
from keras.utils import to_categorical
import numpy as np
from torchvision.io import read_image

categories = ['characters-creatures', 'cultural-heritage-history', 'furniture-home', 'art-abstract', 
                  'science-technology', 'architecture', 'cars-vehicles', 'places-travel', 'people', 'food-drink',
                  'fashion-style', 'sports-fitness', 'music', 'news-politics', 'animals-pets', 'nature-plants',
                  'electronic-gadgets', 'weapons-military']
dict_cat = {k:i for k,i in zip(categories, range(len(categories)))}
#Learning Rate Annealer


X = []
y = []
annotations = objaverse.load_annotations()
print(join(dirname(dirname(__file__)), 'views/'))
count = 0
for dirname1, _, filenames in os.walk(join(dirname(dirname(__file__)), 'views/')):
    for filename in filenames:
       count +=1
       filepath = join(dirname(dirname(__file__)), dirname1, filename)
       img = read_image(filepath)
       X.append(img)
       fs = dirname1.split('/')[-1]
       if len(annotations[fs]['categories']) == 1:
            cat = annotations[fs]['categories'][0]['name']       
            y.append(dict_cat[cat])
       elif len(annotations[fs]['categories']) == 2:
            cat = annotations[fs]['categories'][1]['name']
            y.append(dict_cat[cat])

X = np.array(X)
#print(X.shape)
#print(len(y))
#print(count)
print(y)

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(X,y, test_size=0.3)

x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.3)


y_train=to_categorical(y_train)
y_test=to_categorical(y_test)
y_val = to_categorical(y_val)

from keras.preprocessing.image import ImageDataGenerator

train_generator = ImageDataGenerator(rotation_range=2, horizontal_flip=True,zoom_range=.1 )
test_generator = ImageDataGenerator(rotation_range=2, horizontal_flip= True,zoom_range=.1)
val_generator = ImageDataGenerator(rotation_range=2, horizontal_flip= True,zoom_range=.1)

train_generator.fit(x_train)
test_generator.fit(x_test)
val_generator.fit(x_val)

from keras.callbacks import ReduceLROnPlateau
lrr= ReduceLROnPlateau(   monitor='val_acc',   factor=.01,   patience=3,  min_lr=1e-5) 

batch_size= 100
epochs=100
learn_rate=.001

np.random.seed(1000)

#Instantiation
AlexNet = Sequential()

#1st Convolutional Layer
AlexNet.add(Conv2D(filters=96, input_shape=(227,227,3), kernel_size=(11,11), strides=(4,4), padding='same'))
AlexNet.add(BatchNormalization())
AlexNet.add(Activation('relu'))
AlexNet.add(MaxPooling2D(pool_size=(2,2), strides=(2,2), padding='same'))

#2nd Convolutional Layer
AlexNet.add(Conv2D(filters=256, kernel_size=(5, 5), strides=(1,1), padding='same'))
AlexNet.add(BatchNormalization())
AlexNet.add(Activation('relu'))
AlexNet.add(MaxPooling2D(pool_size=(2,2), strides=(2,2), padding='same'))

#3rd Convolutional Layer
AlexNet.add(Conv2D(filters=384, kernel_size=(3,3), strides=(1,1), padding='same'))
AlexNet.add(BatchNormalization())
AlexNet.add(Activation('relu'))

#4th Convolutional Layer
AlexNet.add(Conv2D(filters=384, kernel_size=(3,3), strides=(1,1), padding='same'))
AlexNet.add(BatchNormalization())
AlexNet.add(Activation('relu'))

#5th Convolutional Layer
AlexNet.add(Conv2D(filters=256, kernel_size=(3,3), strides=(1,1), padding='same'))
AlexNet.add(BatchNormalization())
AlexNet.add(Activation('relu'))
AlexNet.add(MaxPooling2D(pool_size=(2,2), strides=(2,2), padding='same'))

#Passing it to a Fully Connected layer
AlexNet.add(Flatten())
# 1st Fully Connected Layer
AlexNet.add(Dense(4096, input_shape=(32,32,3,)))
AlexNet.add(BatchNormalization())
AlexNet.add(Activation('relu'))
# Add Dropout to prevent overfitting
AlexNet.add(Dropout(0.4))

#2nd Fully Connected Layer
AlexNet.add(Dense(4096))
AlexNet.add(BatchNormalization())
AlexNet.add(Activation('relu'))
#Add Dropout
AlexNet.add(Dropout(0.4))

#3rd Fully Connected Layer
AlexNet.add(Dense(1000))
AlexNet.add(BatchNormalization())
AlexNet.add(Activation('relu'))
#Add Dropout
AlexNet.add(Dropout(0.4))

#Output Layer
AlexNet.add(Dense(10))
AlexNet.add(BatchNormalization())
AlexNet.add(Activation('softmax'))

#Model Summary
AlexNet.summary()
AlexNet.compile(loss = keras.losses.categorical_crossentropy, optimizer= 'adam', metrics=['accuracy'])

AlexNet.fit(train_generator.flow(x_train, y_train, batch_size=batch_size),
 epochs = epochs, 
 steps_per_epoch = x_train.shape[0]//batch_size, 
 validation_data = val_generator.flow(x_val, y_val, 
 batch_size=batch_size), validation_steps = 250, verbose=1)


import matplotlib.pyplot as plt
#Plotting the training and validation loss

f,ax=plt.subplots(2,1) #Creates 2 subplots under 1 column

#Assigning the first subplot to graph training loss and validation loss
ax[0].plot(AlexNet.history.history['loss'],color='b',label='Training Loss')
ax[0].plot(AlexNet.history.history['val_loss'],color='r',label='Validation Loss')

#Plotting the training accuracy and validation accuracy
ax[1].plot(AlexNet.history.history['accuracy'],color='b',label='Training  Accuracy')
ax[1].plot(AlexNet.history.history['val_accuracy'],color='r',label='Validation Accuracy')

plt.legend()


