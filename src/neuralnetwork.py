import json
import pandas
import os
import pdb
import sys
import time

from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

# For showing ASL letter_images
import matplotlib.image as mpimg

from leapdata import create_frame_dict

# Add Leap libraries
sys.path.append("..\\lib")
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.append(arch_dir)
import Leap

data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), u'..\\data\\')
single_data_json = 'single.data.json'
twenty_data_json = 'twenty.data.json'
two_hundred_data_json = 'two_hundred.data.json'
full_alphabet_data_json = 'full_alphabet.data.json'
full_alphabet_2_data_json = 'full_alphabet.2.data.json'
full_json = 'full.json'
my_collection_json = 'mine.json'


class HandDataParser:
    def __init__(self, data_index_of_label):
        self.data_index_of_label = data_index_of_label


    def slice(self):
        # Use advanced slicing capabilities of numpy arrays
        # The outer most/top-level commas delimit slices of subsequent dimensions of the n-d array.
        # For example, the first [:, ...] indicates that we want to take a slice including ALL records
        # of the first dimension. Then after that, we get more specific with which of the columns along
        # the 2nd dimension we want to slice.
        # selector = [x for x in range(self.values.shape[1]) if x != data_index_of_label]
        # selector = [4, 5, 6]
        self.data = self.values[:,:-1] # All but the last column
        self.labels = self.values[:,-1:] # The last column

        # Generate a plot of the distribution of one particular datapoint column
        self.dataframe['Index_Distal_x'].hist(bins=600)
        return self.data, self.labels


    def read_file(self, filename):
        self.filename = filename
        print "Reading file: {}".format(self.filename)
        self.dataframe = pandas.read_json(self.filename)

        # self.values is a numpy n-dimensional array
        self.values = self.dataframe.values

def main():
    data_filename = os.path.join(data_dir, my_collection_json)
    parser = HandDataParser(63)
    parser.read_file(data_filename)
    X, Y = parser.slice()

    validation_size = 0.10
    seed = 7
    X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)
    Y_train = Y_train.ravel()
    # Test options and evaluation metric
    scoring = 'accuracy'

    # Spot Check Algorithms
    models = []
    models.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr')))
    models.append(('LDA', LinearDiscriminantAnalysis()))
    models.append(('KNN', KNeighborsClassifier()))
    models.append(('CART', DecisionTreeClassifier()))
    models.append(('NB', GaussianNB()))
    models.append(('SVM', SVC(gamma='auto')))

    # evaluate each model in turn
    results = []
    names = []
    for name, model in models:
        kfold = model_selection.KFold(n_splits=10, random_state=seed)
        cv_results = model_selection.cross_val_score(model, X_train, Y_train.ravel(), cv=kfold, scoring=scoring)
        results.append(cv_results)
        names.append(name)
        # msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
        # print(msg)

    # Train all the different models
    for name, model in models:
        model.fit(X_train, Y_train)

    # Create a dict mapping
    # letter -> image filepath for that ASL letter
    letter_images = {}
    alphabet = map(chr, range(97, 123))
    assets_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), u'..\\assets\\')

    for letter in alphabet:
        filename = '{}_labelled.png'.format(letter)
        filepath = os.path.join(assets_dir, filename)
        letter_images[str(letter)] = filepath

    # Create a controller
    controller = Leap.Controller()

    while True:
        if controller.is_connected:
            frame, frame_id = create_frame_dict(controller) # TODO: Use frame_id
            if frame is not None:
                model_predictions = []
                for name, model in models:
                    # pdb.set_trace()
                    dataframe = pandas.read_json(json.dumps([frame]))
                    prediction = model.predict(dataframe.values)[0]
                    model_predictions.append(prediction)
                # Out of the 5 ML models run, pick the letter that was picked most often
                # This isn't necessarily a good way to pick the letter...
                prediction = max(set(model_predictions), key=model_predictions.count)
                print model_predictions
                prediction = model_predictions[-1]
                img=mpimg.imread(letter_images[prediction])
                imgplot = plt.imshow(img)
                plt.show()

        else:
            print "No controller connected, sleeping..."
        # Delay
        time.sleep(1)



if __name__ == "__main__":
    main()


