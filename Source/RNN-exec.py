import sys, os, re, csv, codecs, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Dense, Input, LSTM, Embedding, Dropout, Activation
from keras.layers import Bidirectional, GlobalMaxPool1D
from keras.models import Model
from keras import initializers, regularizers, constraints, optimizers, layers
import tensorflow as tf


# Definition des paramètres
flags = tf.flags

flags.DEFINE_integer(
    "embed_size", 128,
    "Taille de l'embedding")
flags.DEFINE_integer("max_features", 10000,
                    "Nombre de mots du dictionnaire")
flags.DEFINE_integer("batch_size", 32,
                    "batch size pour l'entrainement du LSTM")
flags.DEFINE_integer("epochs", 2,
                     "nombre d'epochs pour l'entrainement du LSTM")
flags.DEFINE_integer("maxlen", 10000,
                    "Taille maximum des documents (en nombre de mots) en entree")
flags.DEFINE_string("model_name", "RNN_model", "Nom de sauvegarde du modele")

FLAGS = flags.FLAGS

# Import des fichiers contenant les inputs
training_text = pd.read_csv('../Data/Keras_training_text', sep='\|\|', engine = 'python')
training_variants = pd.read_csv('../Data/training_variants')

# Jointure des deux fichiers et suppression des lignes contenant au moins 1 champ vide
training_set = training_text.merge(training_variants, on='ID')
training_set.dropna(axis=0, how = 'any',inplace=True)

# Séparation inputs/targets
y = pd.get_dummies(training_set['Class'])
list_train_texts = training_set['Text']

# Tokenizer
tokenizer = Tokenizer(num_words=FLAGS.max_features)
tokenizer.fit_on_texts(list(list_train_texts))
list_tokenized_train = tokenizer.texts_to_sequences(list_train_texts)
print("Tokenizer Done")

X_t = pad_sequences(list_tokenized_train, maxlen=FLAGS.maxlen)

inp = Input(shape=(FLAGS.maxlen, )) 

# Création du RNN
x = Embedding(FLAGS.max_features, FLAGS.embed_size)(inp)

x = LSTM(60, return_sequences=True,name='lstm_layer')(x)

x = GlobalMaxPool1D()(x)

x = Dropout(0.1)(x)

x = Dense(50, activation="relu")(x)

x = Dropout(0.1)(x)

x = Dense(9, activation="softmax")(x)

model = Model(inputs=inp, outputs=x)

# Compilation
model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

#Training
model.fit(X_t,y, batch_size=FLAGS.batch_size, epochs=FLAGS.epochs, validation_split=0.1)

model.save(FLAGS.model_name)

