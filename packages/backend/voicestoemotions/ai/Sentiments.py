import gc
import os

import pandas

from keras.layers import Dense, Conv2D, Activation, MaxPooling2D, Dropout, Flatten, BatchNormalization
from keras.models import Sequential
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import EarlyStopping
from keras.constraints import maxnorm


def main():
    gc.collect()

    data_dir = os.path.abspath('../../../../voices-to-emotions')
    index_df = pandas.read_csv(os.path.join(data_dir, 'index_goodbad.csv'))
    class_num = 2

    datagen = ImageDataGenerator(width_shift_range=0.6)

    train = index_df.iloc[:round(len(index_df)*.6)]
    validate = index_df.iloc[round(len(index_df) * .6):]
    test = index_df.iloc[round(len(index_df) * .9):]

    train_generator = datagen.flow_from_dataframe(
        dataframe=train,
        directory=data_dir,
        x_col="file_path",
        y_col="emotion",
        seed=42,
        class_mode="categorical",
        target_size=(223, 221))

    validate_generator = datagen.flow_from_dataframe(
        dataframe=validate,
        directory=data_dir,
        x_col="file_path",
        y_col="emotion",
        seed=42,
        target_size=(223, 221))

    test_generator = datagen.flow_from_dataframe(
        dataframe=test,
        directory=data_dir,
        x_col="file_path",
        y_col="emotion",
        seed=42,
        target_size=(223, 221))

    model = Sequential([
        Conv2D(32, (3, 3), padding='same', input_shape=(223, 221, 3)),
        Activation('relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.3),
        BatchNormalization(),

        Conv2D(64, (3, 3), padding='same', input_shape=(223, 221, 3)),
        Activation('relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.3),
        BatchNormalization(),

        Flatten(),
        Dropout(0.2),

        Dense(256, kernel_constraint=maxnorm(3)),
        Activation('relu'),
        Dropout(0.2),
        BatchNormalization(),

        Dense(128, kernel_constraint=maxnorm(3)),
        Activation('relu'),
        Dropout(0.2),
        BatchNormalization(),

        Dense(class_num),
        Activation('hard_sigmoid'),
        Dropout(0.2),
        BatchNormalization(),

        Activation('relu')
    ])
    model.compile(optimizer=Adam(lr=0.001), loss="categorical_crossentropy", metrics=["accuracy"])
    model.fit_generator(generator=train_generator, validation_data=validate_generator, steps_per_epoch=15,
                        validation_steps=15, epochs=50, use_multiprocessing=True,
                        callbacks=[EarlyStopping(monitor='loss', mode='min', verbose=1, patience=4)])

    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)
    model.save_weights("model.h5")

    print('Model Completed!')
    print('Evaluating model...')

    test_steps = test_generator.n/test_generator.batch_size
    scores = model.evaluate_generator(generator=test_generator, steps=test_steps, verbose=1, use_multiprocessing=True)
    print(scores)
    print("Accuracy %.2f%%" % (scores[1] * 100))


if __name__ == "__main__":
    main()
