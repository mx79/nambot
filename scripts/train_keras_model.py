import json
import random
import numpy as np
import pickle as pkl
import tensorflow as tf
from os.path import abspath, dirname, join

from imblearn.over_sampling import SMOTE

from pkg.clean import clean_text
from keras import Sequential
from keras.layers import Dense, Dropout

# Path
pathdir = dirname(dirname(abspath(__file__)))


def train(model_name: str):

    # Sorting dataset infos
    with open(join(pathdir, "data", "nlu.json"), "r") as f:
        intent_json = json.load(f)
        f.close()
    words = []
    doc_X = []
    for liste in intent_json.values():
        for sent in liste:
            tokens = clean_text(sent, no_accent=False)
            words.extend(tokens)
            doc_X.append(sent)
    doc_y = [k for k, v in intent_json.items() for s in v]
    classes = sorted(set(doc_y))
    vocab = sorted(set(words))

    # Bag of words
    training = []
    out_empty = [0] * len(classes)
    for idx, doc in enumerate(doc_X):
        bow = []
        text = clean_text(doc, no_accent=False)
        for word in vocab:
            bow.append(1) if word in text else bow.append(0)
        output_row = list(out_empty)
        output_row[classes.index(doc_y[idx])] = 1
        training.append([bow, output_row])
    random.shuffle(training)
    training = np.array(training, dtype=object)
    X_train = np.array(list(training[:, 0]))
    y_train = np.array(list(training[:, 1]))

    # Transform the dataset
    oversample = SMOTE()
    X_train, y_train = oversample.fit_resample(X_train, y_train)

    # Some parameters
    input_shape = (len(X_train[0]),)
    output_shape = len(y_train[0])

    # Deep Learning model
    model = Sequential()
    model.add(Dense(128, input_shape=input_shape, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation="relu"))
    model.add(Dropout(0.3))
    model.add(Dense(output_shape, activation="softmax"))
    adam = tf.keras.optimizers.Adam(learning_rate=0.01, decay=1e-6)
    model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=["accuracy"])
    print(model.summary())

    # Model fitting
    model.fit(x=X_train, y=y_train, epochs=200, verbose=1)

    # Saving the model
    pkl.dump(model, open(join(pathdir, "models", model_name + "_keras.pkl"), "wb"))


# Launching the program
if __name__ == "__main__":
    train(input("Nom du modèle à entrainer (stocké dans /models) : "))
