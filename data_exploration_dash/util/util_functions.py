import os
import pickle

#loads a list of all subjects for which data exists
def list_subjects():
    return os.listdir(path='../data/data_raw_from_paper/')

# loads a pickled file using a relative path from the ../data/ directory.
def load_file(data_path):
    with open('../data/' + data_path, "rb") as input_file:
        return pickle.load(input_file)