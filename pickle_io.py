import os
import pickle


def load_pickle(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'rb') as f:
        return pickle.load(f)


def save_pickle(data, filepath):
    with open(filepath, 'wb') as f:
        pickle.dump(data, f)


def picklize(item):
    return str(item) + '.pickle'
