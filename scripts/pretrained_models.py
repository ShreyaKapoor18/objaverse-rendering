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
from torchvision.models import resnet50, ResNet50_Weights
from torchvision.io import read_image
from PIL import Image

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
       print(filepath)
       img = Image.open(filepath)
       X.append(img)
       fs = dirname1.split('/')[-1]
       if len(annotations[fs]['categories']) == 1:
            cat = annotations[fs]['categories'][0]['name']       
            y.append(dict_cat[cat])
       elif len(annotations[fs]['categories']) == 2:
            cat = annotations[fs]['categories'][1]['name']
            y.append(dict_cat[cat])

#X = np.array(X)
#print(X.shape)
print(len(y))
print(count)
#print(y)
print(type(img))
print(img.size)
img = np.array(img)
# remove the alpha channel which is required for the image
print(img.shape)
from torchvision.models import resnet50, ResNet50_Weights

resnet50(weights=ResNet50_Weights.DEFAULT)
resnet50(weights="IMAGENET1K_V1")
resnet50(pretrained=True)
resnet50(True)

weights = ResNet50_Weights.DEFAULT
preprocess = weights.transforms()
batch = preprocess(img).squeeze(0)

# Step 4: Use the model and print the predicted category
prediction = model(batch).unsqueeze(0)
class_id = prediction.argmax().squeeze(0).item()
score = prediction[class_id].item()
category_name = weights.meta["categories"][class_id]
print(f"{category_name}: {100 * score:.1f}%")



