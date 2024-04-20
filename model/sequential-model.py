import os
#import matplotlib.pyplot as plt
from seaborn import set_style
set_style("darkgrid")
import skimage as ski

from skimage.io import imread
from skimage.transform import resize
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import pandas as pd
from keras import models
from keras import layers
from keras import optimizers
from keras import losses
from keras import metrics
from keras import constraints
from keras.utils import to_categorical

from sklearn.metrics import confusion_matrix


# prepare data
input_dir = './'
categories = [str(x) for x in range(2)]

data = []
labels = []
for category_idx, category in enumerate(categories):
    for file in os.listdir(os.path.join(input_dir, category)):
        img_path = os.path.join(input_dir, category, file)
        img = imread(img_path)
        img = ski.color.rgb2gray(img)
        img = resize(img, (320, 320))
        data.append(img) #was img.flatten() for SVM
        labels.append(category_idx)

data = np.asarray(data)
labels = np.asarray(labels)

print(data[901])

x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)



#initialize the model

bigred_model = models.Sequential()


## adding our first convolutional layer

## Conv2D(32, specifies that we want a convolutional layer with depth 32
## (3,3) is our sliding grid size
## We're using the relu activation function
## and our images are a gray scale value for 28X28 pixels, hence the input_shape
bigred_model.add( layers.Conv2D(64, (3,3), activation='relu', input_shape=(320,320,1,)  ) )
bigred_model.add(layers.Dropout(.1))
bigred_model.add( layers.Conv2D(64, (3,3), activation='relu'))
bigred_model.add(layers.Dropout(.1))
## adding our first Max Pooling layer
## MaxPooling2D((2,2) tells python we want to add
## a max pooling layer that uses a (2,2) square grid
## strides = 2, sets the stride value to 2
bigred_model.add( layers.MaxPooling2D( (2,2), strides = 2 ) )


## Add another layer, alternating between conv and pool
bigred_model.add( layers.Conv2D(128, (3,3), activation='relu'))
bigred_model.add(layers.Dropout(.1))
bigred_model.add( layers.Conv2D(128, (3,3), activation='relu'))
bigred_model.add(layers.Dropout(.1))
bigred_model.add( layers.MaxPooling2D( (2,2), strides=2) )


## Add another layer, alternating between conv and pool
bigred_model.add( layers.Conv2D(256, (3,3), activation='relu'))
bigred_model.add(layers.Dropout(.1))
bigred_model.add( layers.Conv2D(256, (3,3), activation='relu'))
bigred_model.add(layers.Dropout(.1))
bigred_model.add( layers.Conv2D(256, (3,3), activation='relu'))
bigred_model.add( layers.AveragePooling2D( (4,4), strides=2) )



## Now we'll add the fully connected layer

## .Flatten() will flatten the data for us,
## meaning the last output data will turn into 
## a vector
bigred_model.add( layers.Flatten() )

## We've seen these before
## Then we add a single dense hidden layer
## This is 64 nodes high
bigred_model.add(layers.Dense(64, activation='relu',kernel_constraint=constraints.MaxNorm(3)))

#dropout layer to reduce overfitting
bigred_model.add(layers.Dropout(.5))


## Finally an output layer
bigred_model.add(layers.Dense(2, activation='softmax'))

#adam or rmsprop?

bigred_model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])


print(bigred_model).summary()


epochs=100


history = bigred_model.fit(x_train, 
                      to_categorical(y_train), 
                      epochs=epochs, 
                      batch_size=32,
                      validation_data=(x_test,to_categorical(y_test)),verbose = 1)

history_dict = history.history




y_pred = bigred_model.predict(x_test)
y_pred = np.argmax(y_pred, axis=1)

print(y_pred[2])



print(pd.DataFrame(confusion_matrix(y_test, y_pred), 
                columns=["predicted "+str(i) for i in range(2)],
                index=["actual "+str(i) for i in range(2)]))