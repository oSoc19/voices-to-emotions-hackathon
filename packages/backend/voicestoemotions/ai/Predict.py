from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
import os
import numpy as np
import pandas as pd


def get_prediction(filepath):
  loaded_model = load_model(os.path.abspath('./model.h5'))
  csv_init = [{'file_path':filepath}]
  df = pd.DataFrame(csv_init)
  df.to_csv("./predict.csv")
  testdf=pd.read_csv('./predict.csv',dtype=str)

  test_datagen=ImageDataGenerator(rescale=1./255.)
  test_gen = test_datagen.flow_from_dataframe(
    dataframe=testdf,
    directory=os.path.abspath(os.path.join(filepath, os.pardir)),
    x_col="file_path",
    y_col=None,
    subset="training",
    batch_size=1,
    class_mode=None,
    target_size=(64, 64)
  )

  pred = loaded_model.predict_generator(test_gen, steps=1, verbose=1)

  emotions = ['angry', 'fearful', 'disgust', 'sad', 'surprised', 'happy', 'calm', 'neutral']

  return emotions[np.argmax(pred, axis=1)[0]]
