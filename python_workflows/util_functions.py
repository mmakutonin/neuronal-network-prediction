import os
import pickle
from datetime import datetime

#loads a list of all subjects for which data exists
def list_subjects():
    return os.listdir(path='../data/data_raw_from_paper/')

# loads a pickled file using a relative path from the ../data/ directory.
def load_file(data_path):
    with open('../data/' + data_path, "rb") as input_file:
        return pickle.load(input_file)

# saves a Python object to a pickled file using a relative path from the ../data/ directory.
def pickle_file(data_path, python_obj):
    with open('../data/' + data_path, 'wb') as pickle_file:
        pickle.dump(python_obj, pickle_file, protocol=pickle.HIGHEST_PROTOCOL)

# returns current system time string
def get_current_time():
    return datetime.now().time()