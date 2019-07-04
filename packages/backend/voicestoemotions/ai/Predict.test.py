import os
import pandas

from Predict import get_prediction

data_dir = os.path.abspath('./dataset')
index_df = pandas.read_csv(os.path.join(data_dir, 'index.csv'))
file_path = os.path.join(data_dir, index_df['file_path'][0])
emotion = index_df['emotion'][0]

predicted_emotion, prediction_values = get_prediction(file_path)

print('Predicted Emotion: ', predicted_emotion)
print('Prediction Values: ', prediction_values)
print('Real Value: ', emotion)
