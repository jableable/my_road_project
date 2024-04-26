import numpy as np
import pandas as pd
from keras import models
from keras import layers
from keras import optimizers
from keras import losses
from keras import constraints
from keras.callbacks import ModelCheckpoint
from keras.utils import image_dataset_from_directory
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.metrics import confusion_matrix

#initialize learning rate and model name
lr = .001
model_name = "binary_classification_model.keras"

#initialize directory location which contains dataset images
input_dir = '../../../../all_coords/'

#initialize batch size and desired image dimensions 
#if dimensions are different than input image, image will be resized
#lowering img height/width reduces quality of image but results in faster/easier training
#make batch size as large as possible to speed up training
batch_size = 64
img_height = 640
img_width = 640

#form train and validation datasets in batches due to large dataset
train_ds = image_dataset_from_directory(
  input_dir,
  validation_split=0.2,
  subset="training",
  seed=123,
  image_size=(img_height, img_width),
  shuffle=True,
  batch_size=batch_size)

val_ds = image_dataset_from_directory(
  input_dir,
  validation_split=0.2,
  subset="validation",
  seed=123,
  image_size=(img_height, img_width),
  shuffle=True,
  batch_size=batch_size)
print("train_ds and val_ds created")

#used in tandem with image_dataset_from_directory to batch load large image set
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

#initialize number of classes
num_classes = 2

#build model with layers
model = models.Sequential([
  layers.InputLayer(shape=(img_height,img_width,3),batch_size=batch_size),
  layers.RandomFlip(mode="horizontal_and_vertical"),
  layers.RandomBrightness(factor=0.2),
  layers.Rescaling(1./255),
  layers.Conv2D(64, (3,3), activation='relu'),
  layers.Dropout(.1),
  layers.MaxPooling2D((2,2), strides=2),
  layers.Conv2D(128, (3,3), activation='relu'),
  layers.Dropout(.1),
  layers.MaxPooling2D((2,2), strides=2),
  layers.Conv2D(256, (3,3), activation='relu'),
  layers.AveragePooling2D((4,4), strides=2),
  layers.Flatten(),
  layers.Dense(128, activation='relu', kernel_constraint=constraints.MaxNorm(3)),
  layers.Dropout(.2),
  layers.Dense(num_classes, activation='softmax')
])

#compile the model
model.compile(optimizer=optimizers.Adam(learning_rate=lr),
              loss=losses.sparse_categorical_crossentropy,
              metrics=['accuracy'])

#save each new best model, where best means highest val_acc
checkpoint = ModelCheckpoint(model_name, save_best_only=True, monitor='val_accuracy', mode='max', verbose=1)

model.summary()

epochs=400

#fit the model
history = model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=epochs,
  verbose=2,
  callbacks=[checkpoint]
)

#load best model to make confusion matrix
checkpoint_model = models.load_model(model_name)

#initialize predicted and true label lists
y_pred = []  
y_true = [] 

#iterate over the dataset
for image_batch, label_batch in val_ds:   
   #append true labels
   y_true.append(label_batch)
   #compute predictions
   preds = checkpoint_model.predict(image_batch, verbose = 0)
   #append predicted labels
   y_pred.append(np.argmax(preds, axis = - 1))

#make and save graph of val_acc and test_acc
plt.figure(figsize = (8,6))
plt.scatter(range(1,epochs+1), history.history['val_accuracy'], label = "Val. Accuracy")
plt.scatter(range(1,epochs+1), history.history['accuracy'], label = "Train Accuracy")
plt.xlabel("Epoch", fontsize=12)
plt.ylabel("Accuracy", fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.legend(fontsize=12)
plt.savefig(str(model_name)+'_acc.png')

# convert the true and predicted labels into tensors
correct_labels = tf.concat([item for item in y_true], axis = 0)
predicted_labels = tf.concat([item for item in y_pred], axis = 0)

#make confusion matrix
print(pd.DataFrame(confusion_matrix(correct_labels,predicted_labels), 
                columns=["predicted "+str(i) for i in range(num_classes)],
                index=["actual "+str(i) for i in range(num_classes)]))