import gc
import os

import numpy
import pandas

from keras.layers import Dense, Embedding, LSTM, Conv1D, MaxPooling1D, Dropout, GRU, Flatten
from keras.models import Sequential
from keras.optimizers import Adam
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from sklearn.model_selection import train_test_split

from nltk.tokenize import word_tokenize
from nltk import FreqDist
from nltk.stem import WordNetLemmatizer

import re

def append_ext(fn):
  return fn + ".png"

def opkuisen(kolom):
    wnl = WordNetLemmatizer()
    toReturn = []
    for x in kolom:
        lijn = str(x)
        lijn = re.sub('[^a-zA-Z]', ' ', lijn)

        lijn_lemmatized = []
        for woord in re.findall(r"[\w']+|[.,!?;]", lijn.lower()):
            lijn_lemmatized.append(wnl.lemmatize(woord))
        lijn = ' '.join(lijn_lemmatized)
        toReturn.append(lijn)
    return toReturn

def main():
    gc.collect()

    data_dir = os.path.abspath('../../../../voices-to-emotions')
    index_df = pandas.read_csv(os.path.join(data_dir, 'index.csv'))

    emotions = ['angry', 'fearful', 'disgust', 'sad', 'happy', 'neutral', 'calm', 'surprised']

    datagen = ImageDataGenerator()

    train, validate, test = numpy.split(index_df.sample(frac=1), [int(.6 * len(index_df)), int(.8 * len(index_df))])

    train_generator = datagen.flow_from_dataframe(
        dataframe=train,
        directory=data_dir,
        x_col="file_path",
        y_col="emotion",
        subset="training",
        batch_size=32,
        seed=42,
        shuffle=True,
        class_mode="categorical",
        target_size=(19, 12))

    validate_generator = datagen.flow_from_dataframe(
        dataframe=validate,
        directory=data_dir,
        x_col="file_path",
        y_col="emotion",
        subset="training",
        batch_size=32,
        seed=42,
        shuffle=True,
        class_mode="categorical",
        target_size=(19, 12))

    test_generator = datagen.flow_from_dataframe(
        dataframe=test,
        directory=data_dir,
        x_col="file_path",
        y_col="emotion",
        subset="training",
        batch_size=32,
        seed=42,
        shuffle=True,
        class_mode="categorical",
        target_size=(19, 12))

    test["Sentiment"] = -1

    temp = pandas.concat([train, test], ignore_index=True) # ignore_index zorgt bij een concat dat de lijnen opnieuw genummerd worden
    del train, test
    gc.collect()

    temp['opgekuist'] = opkuisen(temp.Phrase.values)

    test = temp[temp.Sentiment == -1]
    train = temp[temp.Sentiment != -1]
    test.drop('Sentiment', axis=1, inplace=True)

    del temp
    gc.collect()

    sentimenten = train.Sentiment.values
    cat_sentimenten = to_categorical(sentimenten)

    traintekst = train.opgekuist.values
    testtekst = test.opgekuist.values

    train_kleiner, train_validate, sentimenten_train, sentimenten_validate = train_test_split(traintekst, cat_sentimenten, test_size=0.2, stratify=cat_sentimenten, random_state=42)

    s = word_tokenize(' '.join(train_kleiner))
    aantalwoorden = len(set(s))

    maxlengte = 0
    for t in train_kleiner:
        tok = word_tokenize(t)
        if len(tok) > maxlengte:
            maxlengte = len(tok)

    tz = Tokenizer(num_words=aantalwoorden)
    tz.fit_on_texts(list(train_kleiner))

    model_train = tz.texts_to_sequences(train_kleiner)
    model_train = sequence.pad_sequences(model_train, maxlen=maxlengte)
    model_test = tz.texts_to_sequences(testtekst)
    model_test = sequence.pad_sequences(model_test, maxlen=maxlengte)

    model_validate = tz.texts_to_sequences(train_validate)
    model_validate = sequence.pad_sequences(model_validate, maxlen=maxlengte)

    ### Long Short Term Memory ###

    # LSTM1model = Sequential([
    #     Embedding(aantalwoorden, 250, mask_zero=True),
    #     LSTM(128, dropout=0.4, recurrent_dropout=0.4, return_sequences=False),
    #     Dense(5, activation='softmax')
    # ])

    # Score : 64.401%

    # LSTM2model = Sequential([
    #     Embedding(aantalwoorden, 250, mask_zero=True),
    #     LSTM(128, dropout=0.4, recurrent_dropout=0.4, return_sequences=True),
    #     LSTM(64, dropout=0.5, recurrent_dropout=0.5, return_sequences=False),
    #     Dense(5, activation='softmax')
    # ])

    # Score: 64.758%

    # LSTM3model = Sequential([
    #     Embedding(aantalwoorden, 250, mask_zero=True),
    #     LSTM(128, dropout=0.4, recurrent_dropout=0.4, return_sequences=True),
    #     LSTM(64, dropout=0.5, recurrent_dropout=0.5, return_sequences=True),
    #     LSTM(32, dropout=0.6, recurrent_dropout=0.6, return_sequences=False),
    #     Dense(5, activation='softmax')
    # ])

    # Score: 64.215%


    ### Gated Recurrent Unit ###

    # GRU1model = Sequential([
    #     Embedding(aantalwoorden, 250, mask_zero=True),
    #     GRU(128),
    #     Dense(5, activation='softmax')
    # ])

    # Score: 63.847%

    # GRU2model = Sequential([
    #     Embedding(aantalwoorden, 250, mask_zero=True),
    #     GRU(128, return_sequences=True),
    #     GRU(64, return_sequences=False),
    #     Dense(5, activation='softmax')
    # ])

    # Score: 64.543%

    # GRU3model = Sequential([
    #     Embedding(aantalwoorden, 250, mask_zero=True),
    #     GRU(128, return_sequences=True),
    #     GRU(64, return_sequences=True),
    #     GRU(32, return_sequences=False),
    #     Dense(5, activation='softmax')
    # ])

    ### Convolutional Neural Network ###

    # CNN1model = Sequential([
    # Embedding(aantalwoorden, 100, input_length=maxlengte),
    # Conv1D(64, kernel_size=3, activation='relu'),
    # MaxPooling1D(pool_size=2),
    # Flatten(),
    # Dense(128, activation='relu'),
    # Dropout(0.5),
    # Dense(5, activation='softmax')
    # ])

    # Score: 63.983%

    # CNN2model = Sequential([
    # Embedding(aantalwoorden, 100, input_length=maxlengte),
    # Conv1D(32, kernel_size=3, activation='relu'),
    # MaxPooling1D(pool_size=2),
    # Conv1D(64, kernel_size=3, activation='relu'),
    # MaxPooling1D(pool_size=2),
    # Flatten(),
    # Dense(128, activation='relu'),
    # Dropout(0.5),
    # Dense(5, activation='softmax')
    # ])

    # Score: 56.884%

    # CNN3model = Sequential([
    # Embedding(aantalwoorden, 100, input_length=maxlengte),
    # Conv1D(32, kernel_size=3, activation='relu'),
    # MaxPooling1D(pool_size=2),
    # Conv1D(64, kernel_size=3, activation='relu'),
    # MaxPooling1D(pool_size=2),
    # Conv1D(128, kernel_size=3, activation='relu'),
    # MaxPooling1D(pool_size=2),
    # Flatten(),
    # Dense(128, activation='relu'),
    # Dropout(0.5),
    # Dense(5, activation='softmax')
    # ])

    # Score: 57.329%

    ### CNN + GRU/LSTM ###

    # CNNGRUmodel = Sequential([
    # Embedding(aantalwoorden, 100, input_length=maxlengte),
    # Conv1D(64, kernel_size=3, padding='same', activation='relu'),
    # MaxPooling1D(pool_size=2),
    # Dropout(0.25),
    # GRU(128, return_sequences=True),
    # Dropout(0.3),
    # Flatten(),
    # Dense(128, activation='relu'),
    # Dropout(0.5),
    # Dense(5, activation='softmax')
    # ])

    # Score: 64.665%

    # GRUCNNmodel = Sequential([
    # Embedding(aantalwoorden, 100, input_length=maxlengte),
    # GRU(128, return_sequences=True),
    # Dropout(0.3),
    # Conv1D(64, kernel_size=3, padding='same', activation='relu'),
    # MaxPooling1D(pool_size=2),
    # Flatten()
    # Dense(128, activation='relu'),
    # Dropout(0.5),
    # Dense(5, activation='softmax')
    # ])

    # Score: 64.283%

    # CNNLSTMmodel = Sequential([
    # Embedding(aantalwoorden, 100, input_length=maxlengte),
    # Conv1D(64, kernel_size=3, padding='same', activation='relu'),
    # MaxPooling1D(pool_size=2),
    # Dropout(0.25),
    # LSTM(128, return_sequences=False),
    # Dropout(0.3),
    # Flatten(),
    # Dense(128, activation='relu'),
    # Dropout(0.5),
    # Dense(5, activation='softmax')
    # ])

    # Score: 64.511%

    # LSTMCNNmodel = Sequential([
    # Embedding(aantalwoorden, 100, input_length=maxlengte),
    # LSTM(128, return_sequences=True),
    # Dropout(0.3),
    # Conv1D(64, kernel_size=3, padding='same', activation='relu'),
    # MaxPooling1D(pool_size=2),
    # Flatten()
    # Dense(128, activation='relu'),
    # Dropout(0.5),
    # Dense(5, activation='softmax')
    # ])

    # Score: 64.347%

    LSTM1Model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=0.001), metrics=['accuracy'])

    fitten = LSTM1Model.fit(model_train, sentimenten_train, validation_data=(model_validate, sentimenten_validate), epochs=5, batch_size=128, verbose=1)

    prediction = LSTM1Model.predict_classes(model_test)

    sample.Sentiment = prediction
    sample.to_csv('LSTM1_output.csv', index=False)

if __name__ == "__main__":
    main()
