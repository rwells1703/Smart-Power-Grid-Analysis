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

def train_bagging(curves, labels):
    classifier = sklearn.ensemble.BaggingClassifier(sklearn.svm.SVC(), n_estimators=10000)
    classifier.fit(curves, labels)
    print("Fitted")

    return classifier

# Make predictions based upon training data
def predict(classifier, curves):
    predictions = classifier.predict(curves)
    print("Predicted")

    return predictions

# Compare the predictions against the labels of the training data
def calculate_training_accuracy(predictions, labels):
    correct = 0
    i = 0
    while i < len(predictions):
        if predictions[i] == labels[i]:
            correct += 1
        i += 1

    incorrect = len(predictions)-correct
    accuracy = correct/len(predictions)

    return correct, incorrect, accuracy

# Display training accuracy stats
def display_accuracy(correct, incorrect, accuracy):
    print(f"Correct: {correct}")
    print(f"Incorrect: {incorrect}")
    print(f"Accuracy: {accuracy}")


def main():
    # Load training/validation data from a file
    data = data_load.read_data("data\\TrainingData.txt")

    # Take 10% of values as validation data, and the remaining as training data
    training_data, validation_data = data_load.split_training_validation(data, 0.1)

    # Extract curves and labels from training/verification data
    training_curves, training_labels = data_load.parse_labelled_data(training_data)
    validation_curves, validation_labels = data_load.parse_labelled_data(validation_data)

    #curves = list(map(preprocess_curve_avg, curves))

    # Train the classifier, and perform predictions on validation data
    classifier = train_bagging(training_curves, training_labels)

    predictions = predict(classifier, validation_curves)

    # Display the accuacy results
    correct, incorrect, accuracy = calculate_training_accuracy(predictions, validation_labels)
    display_accuracy(correct, incorrect, accuracy)

if __name__ == "__main__":
    for i in range(1,10):
        main()