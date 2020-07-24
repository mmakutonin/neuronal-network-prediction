import pickle

# loads a pickled file using a relative path from the ../data/ directory.
def load_file(data_path):
    with open('../data/' + data_path, "rb") as input_file:
        return pickle.load(input_file)