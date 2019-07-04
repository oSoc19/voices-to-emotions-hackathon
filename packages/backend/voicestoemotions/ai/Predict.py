from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
import os
import numpy as np
import pandas as pd

def round_pred(n):
    return round(n * 10000) / 10000

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
        batch_size=1,
        class_mode=None,
        target_size=(64, 64)
    )

    pred = loaded_model.predict_generator(test_gen, steps=1, verbose=1)

    emotions = ['angry', 'fearful', 'disgust', 'sad', 'surprised', 'happy', 'calm', 'neutral']

    # TODO: Find a better solution for this. Google Cloud will probably do this for us anyway...
    mapped_emotions = {
        'angry': round_pred(pred[0][0]),
        'fearful': round_pred(pred[0][1]),
        'disgust': round_pred(pred[0][2]),
        'sad': round_pred(pred[0][3]),
        'surprised': round_pred(pred[0][4]),
        'happy': round_pred(pred[0][5]),
        'calm': round_pred(pred[0][6]),
        'neutral': round_pred(pred[0][7])
    }

    return emotions[np.argmax(pred, axis=1)[0]], mapped_emotions
