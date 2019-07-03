import gc
import os

import numpy
import pandas

from keras.layers import Dense, Conv2D, Activation, MaxPooling2D, Dropout, Flatten
from keras.models import Sequential
from keras.optimizers import Adam
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
import tensorflow
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split

from nltk.tokenize import word_tokenize
from nltk import FreqDist
from nltk.stem import WordNetLemmatizer

import re

def main():
    gc.collect()

    data_dir = os.path.abspath('../../../../voices-to-emotions/voices-to-emotions-dataset')
    index_df = pandas.read_csv(os.path.join(data_dir, 'index.csv'))

    # emotions = ['angry', 'fearful', 'disgust', 'sad', 'happy', 'neutral', 'calm', 'surprised']

    datagen = ImageDataGenerator(width_shift_range=0.6)

    train, validate, test = numpy.split(index_df.sample(frac=1), [int(.6 * len(index_df)), int(.8 * len(index_df))])

    train_generator = datagen.flow_from_dataframe(
        dataframe=train,
        directory=data_dir,
        x_col="file_path",
        y_col="emotion",
        subset="training",
        seed=42,
        class_mode="categorical",
        target_size=(223, 221))

    validate_generator = datagen.flow_from_dataframe(
        dataframe=validate,
        directory=data_dir,
        x_col="file_path",
        y_col="emotion",
        subset="validation",
        seed=42,
        target_size=(223, 221))

    # test_generator = datagen.flow_from_dataframe(
    #     dataframe=test,
    #     directory=data_dir,
    #     x_col="file_path",
    #     y_col="emotion",
    #     seed=42,
    #     target_size=(223, 221))

    model = Sequential([
    Conv2D(32, (3, 3), padding='same', input_shape=(223, 221, 3)),
    Activation('relu'),
    Conv2D(64, (3, 3)),
    Activation('relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.25),
    Conv2D(64, (3, 3), padding='same'),
    Activation('relu'),
    Conv2D(64, (3, 3)),
    Activation('relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.5),
    Conv2D(128, (3, 3), padding='same'),
    Activation('relu'),
    Conv2D(128, (3, 3)),
    Activation('relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.5),
    Flatten(),
    Dense(512),
    Activation('relu'),
    Dropout(0.5),
    Dense(8, activation='softmax')])

    model.compile(optimizer=Adam(lr=0.001), loss="categorical_crossentropy", metrics=["accuracy"])
    model.fit_generator(generator=train_generator, validation_data=validate_generator, steps_per_epoch=(train_generator.n // train_generator.batch_size), validation_steps=(train_generator.n // train_generator.batch_size), epochs=150, callbacks=[EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=5)])

    model_json = model.to_json()
    with open("model.json", "w") as json_file:
      json_file.write(model_json)
    model.save_weights("model.h5")

if __name__ == "__main__":
    main()
