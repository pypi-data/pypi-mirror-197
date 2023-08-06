import pickle


def to_pickle(_obj, path, **kwargs):
    pickle.dump(_obj, open(path, "wb"))


def read_pickle(path):
    pickle.load(open(path, "rb"))

