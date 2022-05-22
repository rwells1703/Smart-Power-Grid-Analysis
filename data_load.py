import csv
from matplotlib import pyplot as plt
import random

# Read data from file
def read_data(filepath):
    with open(filepath) as file:
        # Read the CSV file data
        reader = csv.reader(file)

        data = []
        # Store each line of the data into a list
        for row in reader:
            data.append([float(v) for v in row])

    return data

# Convert the training (or verification) data into 
# lists containing the curves and the labels
def parse_labelled_data(data):
    # Parse the data into curves and labels
    curves = list(map(lambda c: c[:-1], data))
    labels = list(map(lambda c: c[-1], data))

    return curves, labels

# Split labelled data into training and validation data sets
def split_training_validation(data, target_proportion, seed=-1):
    data_len = len(data)

    if seed != -1:
        random.seed(seed)

    validation_data = []
    proportion = 0
    while proportion < target_proportion:
        i = random.randint(0, len(data)-1)
        validation_data.append(data.pop(i))
        proportion = len(validation_data)/data_len
    
    return data, validation_data
    
# Save the training data curves and labels as images
def save_training_images(curves, labels):
    for i in range(len(curves)):
        if labels[i] == 0.0:
            color = "#076300"
        else:
            color = "#bf0202"

        plt.plot(range(len(curves[i])), curves[i], c=color)
        plt.savefig(f"figures\\training\\{i}({labels[i]}).jpg")
        plt.close()

# Save the testing data curves as images
def save_testing_images(curves):
    for i in range(len(curves)):
        plt.plot(range(len(curves[i])), curves[i])
        plt.savefig(f"figures\\testing\\{i}.jpg")
        plt.close()