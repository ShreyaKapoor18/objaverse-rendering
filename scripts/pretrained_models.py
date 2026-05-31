#%%
import numpy as np
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
from torchvision.models import resnet50, ResNet50_Weights
from torchvision.io import read_image
import torch
#%%
# https://vitalflux.com/pytorch-load-predict-pretrained-resnet-model/
categories = ['characters-creatures', 'cultural-heritage-history', 'furniture-home', 'art-abstract', 
                  'science-technology', 'architecture', 'cars-vehicles', 'places-travel', 'people', 'food-drink',
                  'fashion-style', 'sports-fitness', 'music', 'news-politics', 'animals-pets', 'nature-plants',
                  'electronics-gadgets', 'weapons-military']
dict_cat = {k:i for k,i in zip(categories, range(len(categories)))}
#Learning Rate Annealer
#%%
'''
X = []
y = []
annotations = objaverse.load_annotations()
print(join(dirname(dirname(__file__)), 'views/'))
count = 0
for dirname1, _, filenames in os.walk(join(dirname(dirname(__file__)), 'views/')):
    for filename in filenames:
       count +=1
       filepath = join(dirname(dirname(__file__)), dirname1, filename)
       img = Image.open(filepath).convert("RGB")
       X.append(img)
       fs = dirname1.split('/')[-1]
       if len(annotations[fs]['categories']) == 1:
            cat = annotations[fs]['categories'][0]['name']       
            y.append(dict_cat[cat])
       elif len(annotations[fs]['categories']) == 2:
            cat = annotations[fs]['categories'][1]['name']
            y.append(dict_cat[cat])
'''
#%%
filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'views', 'cars-vehicles', 'e9fe70b8fc094d26a08bb4b8c1c37518', '008.png')
img = Image.open(filepath).convert("RGB")
#X = np.array(X)
#print(X.shape)
plt.imshow(img)
print(filepath)
resnet = resnet50(weights=ResNet50_Weights.DEFAULT)
from torchvision import transforms
#
# Create a preprocessing pipeline
#
preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )])
#%%
# Pass the image for preprocessing and the image preprocessed
img_preprocessed = preprocess(img)
batch_tensor = torch.unsqueeze(img_preprocessed, 0)
resnet.eval()
out = resnet(batch_tensor)

with open('imagenet_classes.txt') as f:
    labels = [line.strip() for line in f.readlines()]

_, index = torch.max(out, 1)#
percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100
#
# Print the name along with score of the object identified by the model
#
print(labels[index[0]], percentage[index[0]].item())
#
# Print the top 5 scores along with the image label. Sort function is invoked on the torch to sort the scores.
#
_, indices = torch.sort(out, descending=True)
[(labels[idx], percentage[idx].item()) for idx in indices[0][:5]]
