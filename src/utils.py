from src.consts import ROOT_PATH


def open_file(filename, file_extension):
    with open(ROOT_PATH + filename + file_extension) as f:
        return f.readlines()
