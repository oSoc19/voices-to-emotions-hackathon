from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
import os
import numpy as np
import pandas as pd


def get_prediction(filepath):
    dir = os.path.dirname(filepath)
    file_name = os.path.basename(filepath)

    df = pd.DataFrame([{'file_path': file_name}])

    loaded_model = load_model(os.path.abspath('./model.h5'))

    test_datagen = ImageDataGenerator(rescale=1. / 255.)
    test_gen = test_datagen.flow_from_dataframe(
        dataframe=df,
        directory=dir,
        x_col="file_path",
        y_col=None,
        subset="training",
        batch_size=1,
        class_mode=None,
        target_size=(64, 64)
    )

    pred = loaded_model.predict_generator(test_gen, steps=1, verbose=1)

    print('Predictions')
    print(pred)

    emotions = ['angry', 'fearful', 'disgust', 'sad', 'surprised', 'happy', 'calm', 'neutral']

    return emotions[np.argmax(pred, axis=1)[0]]
