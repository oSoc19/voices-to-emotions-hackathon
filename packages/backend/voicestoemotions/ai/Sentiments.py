import gc
import os

import pandas

from keras.layers import Dense, Conv2D, Activation, MaxPooling2D, Dropout, Flatten, BatchNormalization
from keras.models import Sequential
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import EarlyStopping


def main():
    gc.collect()

    data_dir = os.path.abspath('./dataset')
    index_df = pandas.read_csv(os.path.join(data_dir, 'index.csv'))

    datagen = ImageDataGenerator(rescale=1. / 255., validation_split=0.25)

    train = index_df.iloc[:round(len(index_df) * .6)]
    validate = index_df.iloc[round(len(index_df) * .6):]
    test = index_df.iloc[round(len(index_df) * .9):]

    train_generator = datagen.flow_from_dataframe(
        dataframe=train,
        directory=data_dir,
        x_col="file_path",
        y_col="emotion",
        batch_size=32,
        seed=42,
        shuffle=True,
        class_mode="categorical",
        target_size=(64, 64))

    validate_generator = datagen.flow_from_dataframe(
        dataframe=validate,
        directory=data_dir,
        x_col="file_path",
        y_col="emotion",
        batch_size=32,
        seed=42,
        shuffle=True,
        class_mode="categorical",
        target_size=(64, 64))

    test_generator = datagen.flow_from_dataframe(
        dataframe=test,
        directory=data_dir,
        x_col="file_path",
        y_col="emotion",
        batch_size=32,
        seed=42,
        shuffle=True,
        class_mode="categorical",
        target_size=(64, 64))

    model = Sequential()

    model.add(Conv2D(32, (3, 3), padding='same', input_shape=(64, 64, 3)))
    model.add(Activation('relu'))

    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(Activation('relu'))

    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.5))

    model.add(Conv2D(128, (3, 3), padding='same'))
    model.add(Activation('relu'))

    model.add(Conv2D(128, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.5))

    model.add(Flatten())
    model.add(Dense(512))

    model.add(Activation('hard_sigmoid'))
    model.add(Dropout(0.5))

    model.add(Dense(8, activation='softmax'))

    model.compile(optimizer=Adam(lr=0.001), loss="categorical_crossentropy", metrics=["accuracy"])
    model.summary()

    step_size_generator = train_generator.n // train_generator.batch_size
    step_size_validate = validate_generator.n // validate_generator.batch_size

    model.fit_generator(
        generator=train_generator,
        validation_data=validate_generator,
        steps_per_epoch=step_size_generator,
        validation_steps=step_size_validate,
        epochs=100,
        use_multiprocessing=True,
        callbacks=[EarlyStopping(monitor='loss', mode='min', verbose=1, patience=5)]
    )

    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)
    model.save_weights("model.h5")

    print('Model Completed!')
    print('Evaluating model...')

    test_steps = test_generator.n / test_generator.batch_size
    scores = model.evaluate_generator(generator=test_generator, steps=test_steps, verbose=1, use_multiprocessing=True)
    print(scores)
    print("Accuracy %.2f%%" % (scores[1] * 100))


if __name__ == "__main__":
    main()
