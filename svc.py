import numpy as np
import random
from sklearn.model_selection import GridSearchCV
import sklearn.svm
import sklearn.ensemble

import data_load

# Average, applied to each curve in the data before it is used for fitting/prediction
def preprocess_curve_avg(curve):
    average = sum(curve)/len(curve)
    curve = [average]

    return curve

# Fit the classifier to the training data
def train(curves, labels):
    classifier = sklearn.svm.SVC()
    classifier.fit(curves, labels)
    print("Fitted")

    return classifier

# Fit the classifier to the training data using optimized C and Gamma
def train_optimized(curves, labels):
    classifier = sklearn.svm.SVC(C=10, gamma=0.1)
    classifier.fit(curves, labels)
    print("Fitted")

    return classifier

# Fit the classifier (with bagging) to the training data
def train_bagging(curves, labels):
    classifier = sklearn.ensemble.BaggingClassifier(sklearn.svm.SVC(), n_estimators=100)
    classifier.fit(curves, labels)
    print("Fitted")

    return classifier

# Try many different parameters of C and gamma to maximise the accuracy
def find_optimized_params(curves, labels):
    # Possible values of C and Gamma listed
    param_grid = [{'C': [0.01, 0.1, 1, 10, 100], 'gamma': [0.01, 0.1, 1, 10, 100], 'kernel': ['rbf']}]
    classifier = GridSearchCV(sklearn.svm.SVC(), param_grid, verbose=3)
    classifier.fit(curves, labels)
    print("Fitted")

    print("Parameters:")
    print(classifier.best_params_)
    print(classifier.best_score_)
    print(classifier.best_estimator_)

    return classifier.best_estimator_

# Make predictions based upon training data
def predict(classifier, curves):
    predictions = classifier.predict(curves)
    print("Predicted")

    return predictions

# Compare the predictions against the labels of the data
def calculate_accuracy(predictions, labels):
    correct_nums = []
    correct = 0
    i = 0
    while i < len(predictions):
        if predictions[i] == labels[i]:
            correct += 1
            correct_nums += "y"
        else:
            correct_nums += "n"
        i += 1
    print(correct_nums)

    incorrect = len(predictions)-correct
    accuracy = correct/len(predictions)

    return correct, incorrect, accuracy

# Display accuracy stats for predictions on labelled data
def display_accuracy(correct, incorrect, accuracy):
    print(f"Correct: {correct}")
    print(f"Incorrect: {incorrect}")
    print(f"Accuracy: {accuracy}")

# Display the predictions, along with the number of 1s and 0s respectively
def display_predictions(predictions):
    print(predictions)
    print(f"1: {np.count_nonzero(predictions == 1.0)}")
    print(f"0: {np.count_nonzero(predictions == 0.0)}")

# Return the index numbers of every pricing curve that is predicted to be abnormal
def get_abormal_curves(predictions):
    indexes = []
    for i in range(len(predictions)):
        if predictions[i] == 1.0:
            indexes.append(i)
    return indexes

# Save the prediction array to a file in CSV format
def save_predictions(predictions):
    with open("results\\results.csv","a") as f:
        predictions = map(str, predictions)
        f.write(",".join(predictions)+"\n")

# Save each testing curve followed by its classification (1 or 0) in CSV format
def save_testing_results(curves, predictions):
    i = 0
    while i < len(curves):
        curves[i].append(int(predictions[i]))
        i += 1

    with open("results\\TestingResults.txt","w") as f:
        for c in curves:
            c = map(str, c)
            f.write(",".join(c)+"\n")

# Perform predictions and accuracy testing on the training data (already seen before)
def predict_training_data():
    # Load training data from a file
    training_data = data_load.read_data("data\\TrainingData.txt", "f*")
    random.shuffle(training_data)

    # Extract curves and labels from training data
    training_curves, training_labels = data_load.parse_labelled_data(training_data)

    # Train the classifier, and perform predictions on training data
    classifier = train_bagging(training_curves, training_labels)
    predictions = predict(classifier, training_curves)
    display_predictions(predictions)
    
    # Display the accuacy results
    correct, incorrect, accuracy = calculate_accuracy(predictions, training_labels)
    display_accuracy(correct, incorrect, accuracy)

    return predictions, training_curves

# Perform predictions and accuracy testing on a "validation" subset of the training data
def predict_validation_data():
    # Load training and validation data from a file
    data = data_load.read_data("data\\TrainingData.txt", "f*")
    random.shuffle(data)

    # Take 10% of values as validation data, and the remaining as training data
    training_data, validation_data = data_load.split_training_validation(data, 0.2, 123)

    # Extract curves and labels from training/verification data
    training_curves, training_labels = data_load.parse_labelled_data(training_data)
    validation_curves, validation_labels = data_load.parse_labelled_data(validation_data)

    # Train the classifier, and perform predictions on validation data
    classifier = train(training_curves, training_labels)
    predictions = predict(classifier, validation_curves)
    display_predictions(predictions)

    # Display the accuacy results
    correct, incorrect, accuracy = calculate_accuracy(predictions, validation_labels)
    display_accuracy(correct, incorrect, accuracy)

    return predictions, validation_curves

# Perform predictions on the testing data
def predict_testing_data(save=False):
    # Load training data from a file
    training_data = data_load.read_data("data\\TrainingData.txt", "f*")
    random.shuffle(training_data)

    # Extract curves and labels from training data
    training_curves, training_labels = data_load.parse_labelled_data(training_data)

    # Train the classifier
    classifier = train(training_curves, training_labels)

    # Load testing data from a file
    testing_curves = data_load.read_data("data\\TestingData.txt", "f*")

    # Perform predictions on testing data
    predictions = predict(classifier, testing_curves)

    # Display and save results
    display_predictions(predictions)
    if save:
        save_testing_results(testing_curves, predictions)

    return predictions, testing_curves

def main():
    #predictions, curves = predict_testing_data(save=True)
    predictions, curves = predict_validation_data()

if __name__ == "__main__":
    main()