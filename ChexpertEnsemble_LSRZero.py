# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1B9VOn4PZ_kuT9BIjYz4V8CsNeYxHk4z9
"""

import cv2
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
from tqdm import tqdm, tqdm_notebook
from keras.models import Model
from keras.layers import Dropout, Flatten, Dense
from tensorflow.keras import optimizers
from keras.applications import Xception
import tensorflow as tf
from sklearn.model_selection import train_test_split
from keras.applications import InceptionResNetV2
from keras.applications.densenet import DenseNet121
import numpy as np
import keras
from keras.models import Sequential, Model
from keras.layers import Dense, Flatten, Activation, Dropout, GlobalAveragePooling2D
from keras_preprocessing.image import ImageDataGenerator
from keras import  applications
from keras.callbacks import ModelCheckpoint, LearningRateScheduler, TensorBoard, EarlyStopping
from keras import backend as K 
from sklearn.datasets.samples_generator import make_blobs
from sklearn.metrics import accuracy_score
from keras.models import load_model
from keras.utils import to_categorical
from keras.utils import plot_model
from keras.layers import Input
from keras.layers.merge import concatenate
from numpy import argmax
from keras_efficientnets import EfficientNetB0
from keras.models import load_model
features=['Cardiomegaly', 'Edema', 'Consolidation', 'Pleural Effusion','Atelectasis']
image_size=224
data_path='/content/Chexperttraining1'
data=pd.read_csv('/content/Processed_train.csv')
def load_inception():
  base_model = InceptionResNetV2(include_top= False, input_shape=(image_size,image_size,3), weights='imagenet')
  # add a global spatial average pooling layer
  x = base_model.output

  #test=pd.read_csv('/content/Processed_test.csv')#testing data
  x = GlobalAveragePooling2D(input_shape=(1024,1,1))(x)
  # Add a flattern layer 
  x = Dense(2048, activation='relu')(x)
  x = keras.layers.normalization.BatchNormalization()(x)
  x = Dropout(0.2)(x)
  # Add a fully-connected layer
  x = Dense(512, activation='relu')(x)
  x = keras.layers.normalization.BatchNormalization()(x)
  x = Dropout(0.2)(x)
  # and a logistic layer --  we have 5 classes
  predictions = Dense(5, activation='sigmoid')(x)

  # this is the model we will train
  model = Model(inputs=base_model.input, outputs=predictions)
  model.load_weights('InceptionResNetmodelLSRZero_bestauc.hdf5')
  return model

def load_Xception():
  base_model = Xception(include_top= False, input_shape=(image_size,image_size,3), weights='imagenet')
  # add a global spatial average pooling layer
  x = base_model.output
  x = GlobalAveragePooling2D(input_shape=(1024,1,1))(x)
  # Add a flattern layer 
  x = Dense(2048, activation='relu')(x)
  x = keras.layers.normalization.BatchNormalization()(x)
  x = Dropout(0.2)(x)
  # Add a fully-connected layer
  x = Dense(512, activation='relu')(x)
  x = keras.layers.normalization.BatchNormalization()(x)
  x = Dropout(0.2)(x)
  # and a logistic layer --  we have 5 classes
  predictions = Dense(5, activation='sigmoid')(x)

  # this is the model we will train
  model = Model(inputs=base_model.input, outputs=predictions)
  model.load_weights('Xception_LSRZerobestauc.hdf5')
  return model

def load_efficientnet():
  base_model = EfficientNetB0(include_top= False, input_shape=(image_size,image_size,3), weights='imagenet')
  # add a global spatial average pooling layer
  x = base_model.output


  x = GlobalAveragePooling2D(input_shape=(1024,1,1))(x)
  # Add a flattern layer 
  x = Dense(2048, activation='relu')(x)
  x = keras.layers.normalization.BatchNormalization()(x)
  x = Dropout(0.2)(x)
  # Add a fully-connected layer
  x = Dense(512, activation='relu')(x)
  x = keras.layers.normalization.BatchNormalization()(x)
  x = Dropout(0.2)(x)
  # and a logistic layer --  we have 5 classes
  predictions = Dense(5, activation='sigmoid')(x)

  # this is the model we will train
  model = Model(inputs=base_model.input, outputs=predictions)
  model.load_weights('EffiecientNetLSRZero_bestauc.hdf5')
  return model

def generate_generator_multiple(generator,dir1, dir2, batch_size, img_height,img_width):
    genX1=generator.flow_from_dataframe(dataframe=data, directory=data_path, 
																										x_col='Path', y_col=features, seed = 42, 
																										class_mode='raw', target_size=(image_size,image_size), batch_size=32, subset = "training")
    genX2 =generator.flow_from_dataframe(dataframe=data, directory=data_path, 
																										x_col='Path', y_col=features, seed = 42, 
																										class_mode='raw', target_size=(image_size,image_size), batch_size=32, subset = "training")
                
    genX3 = generator.flow_from_dataframe(dataframe=data, directory=data_path, 
																										x_col='Path', y_col=features, seed = 42, 
																										class_mode='raw', target_size=(image_size,image_size), batch_size=32, subset = "training")
    while True:
            X1i = genX1.next()
            X2i = genX2.next()
            X3i = genX3.next()
            yield [X1i[0], X2i[0],X3i[0]], X2i[1]  #Yield both images and their mutual label
def valid_generator_multiple(generator,dir1, dir2, batch_size, img_height,img_width):
    genX1=generator.flow_from_dataframe(dataframe=data, directory=data_path, 
																										x_col='Path', y_col=features, seed = 42, 
																										class_mode='raw', target_size=(image_size,image_size), batch_size=32, subset = "validation")
    genX2 =generator.flow_from_dataframe(dataframe=data, directory=data_path, 
																										x_col='Path', y_col=features, seed = 42, 
																										class_mode='raw', target_size=(image_size,image_size), batch_size=32, subset = "validation")     
    genX3 = generator.flow_from_dataframe(dataframe=data, directory=data_path, 
																										x_col='Path', y_col=features, seed = 42, 
																										class_mode='raw', target_size=(image_size,image_size), batch_size=32, subset = "validation")
    while True:
            X1i = genX1.next()
            X2i = genX2.next()
            X3i = genX3.next()
            yield [X1i[0], X2i[0],X3i[0]], X2i[1]  #Yield both images and their mutual label


 
# define stacked model from multiple member input models
def define_stacked_model(members):
	# update all layers in all models to not be trainable
	for i in range(len(members)):
		model = members[i]
		for layer in model.layers:
			# make not trainable
			layer.trainable = False
			# rename to avoid 'unique layer name' issue
			layer.name = 'ensemble_' + str(i) + '_' + layer.name
	# define multi-headed input
	ensemble_visible = [model.input for model in members]
	# concatenate merge output from each model
	ensemble_outputs = [model.output for model in members]
	merge = concatenate(ensemble_outputs)
	hidden = Dense(10, activation='relu')(merge)
	output = Dense(5, activation='sigmoid')(hidden)
	model = Model(inputs=ensemble_visible, outputs=output)
	# plot graph of ensemble
	plot_model(model, show_shapes=True, to_file='model_graph.png')
	# compile
	#STEP_SIZE_TRAIN=train_generator.n//train_generator.batch_size
	#STEP_SIZE_VALID=valid_generator.n//valid_generator.batch_size
	lr_schedule = optimizers.schedules.ExponentialDecay(
	initial_learning_rate=1e-3,
	decay_steps=5026,
	decay_rate=0.1)
	optimizer = optimizers.Adam(learning_rate=lr_schedule)
	model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy',tf.keras.metrics.AUC(multi_label=True)])
	
	return model
 
# fit a stacked model
def fit_stacked_model(model):
		# prepare input data
		data_path='/content/Chexperttraining1'
		data=pd.read_csv('/content/Processed_train_LSR-Zeros.csv')
		#X = [inputX for _ in range(len(model.input))]
		# encode output data
		#inputy_enc = to_categorical(inputy)
		# fit model
		datagen=ImageDataGenerator(rescale=1./255,samplewise_center=True, samplewise_std_normalization=True, 
															rotation_range=5,
															width_shift_range=0.2,
															height_shift_range=0.2,
															horizontal_flip=True,
															validation_split = 0.25)
    #test_datagen=ImageDataGenerator(rescale=1./255)
		img_height=224
		image_size=224
		batch_size=32

	
		valid_generator=datagen.flow_from_dataframe(dataframe=data, directory=data_path, 
																										x_col='Path', y_col=features, seed = 42, 
																										class_mode='raw', target_size=(image_size,image_size), batch_size=32, subset = "validation")
		train_generator=datagen.flow_from_dataframe(dataframe=data, directory=data_path, 
																										x_col='Path', y_col=features, seed = 42, 
																										class_mode='raw', target_size=(image_size,image_size), batch_size=32, subset = "training")
		STEP_SIZE_TRAIN=train_generator.n//train_generator.batch_size
		STEP_SIZE_VALID=valid_generator.n//valid_generator.batch_size

		inputgenerator=generate_generator_multiple(generator=datagen,
																							dir1=data_path,
																							dir2=data_path,
																							batch_size=batch_size,
																							img_height=img_height,
																							img_width=img_height)       
				
		testgenerator=valid_generator_multiple(generator=datagen,
																							dir1=data_path,
																							dir2=data_path,
																							batch_size=batch_size,
																							img_height=img_height,
																							img_width=img_height)              
		epochs=22					
		checkpointer = ModelCheckpoint(filepath='ensemble_best_auc_LSRZero.hdf5', 
															verbose=1, save_best_only=True,monitor='val_auc',mode='max')
		checkpointer1=ModelCheckpoint(filepath='ensemble_best_acc_LSRZero.hdf5', 
																verbose=1, save_best_only=True,monitor='val_accuracy',mode='max')

		history=model.fit_generator(inputgenerator,
														steps_per_epoch=STEP_SIZE_TRAIN,
														epochs = epochs,
														callbacks = [checkpointer,checkpointer1],
														validation_data = testgenerator,
														validation_steps = STEP_SIZE_VALID,
														use_multiprocessing=True,
														shuffle=False)

# make a prediction with a stacked model
def predict_stacked_model(model, inputX):
	# prepare input data
	X = [inputX for _ in range(len(model.input))]
	# make prediction
	return model.predict(X, verbose=1)

# load all models

n_members = 3
model1=load_Xception()
model1.layers.pop()
model1.layers.pop()
model1.layers.pop()
model2=load_efficientnet()
model2.layers.pop()
model2.layers.pop()
model2.layers.pop()
model3=load_inception()
model3.layers.pop()
model3.layers.pop()
model3.layers.pop()
all_models=[model1,model2,model3]
members = all_models
#load_all_models(n_members)
print('Loaded %d models' % len(members))
# define ensemble model
stacked_model = define_stacked_model(members)
fit_stacked_model(stacked_model)