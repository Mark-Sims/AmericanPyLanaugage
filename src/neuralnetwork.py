import json
import pandas
import os
import pdb


data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), u'..\\data\\')
single_data_json = 'single.data.json'
twenty_data_json = 'twenty.data.json'

class HandDataParser:
    def __init__(self, filename, data_index_of_label):
        self.filename = filename
        self.data_index_of_label = data_index_of_label

        self.read_file()
        # Values is a numpy n-dimensional array
        self.values = self.dataframe.values

        # Use advanced slicing capabilities of numpy arrays
        # The outermost/top-level commas delimit slices of subsequent dimensions of the n-d array.
        # For example, the first [:, ...] indicates that we want to take a slice including ALL records
        # of the first dimension. Then after that, we get more specific with which of the columns along
        # the 2nd dimension we want to slice.
        selector = [x for x in range(self.values.shape[1]) if x != data_index_of_label]
        selector = [4, 5, 6]
        self.data = self.values[:,selector]
        self.labels = self.values[:,1]
        pdb.set_trace()


    def read_file(self):
        print "Reading file: {}".format(self.filename)
        self.dataframe = pandas.read_json(self.filename)



def main():
    data_filename = os.path.join(data_dir, twenty_data_json)
    parser = HandDataParser(data_filename, 1)


if __name__ == "__main__":
    main()


