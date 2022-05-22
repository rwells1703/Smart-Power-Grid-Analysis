import sklearn.svm

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
    data = data_load.read_data("data\\TrainingData.txt")
    curves, labels = data_load.parse_training_data(data)
    curves = list(map(preprocess_curve_avg, curves))
    classifier = train(curves, labels)
    predictions = predict(classifier, curves)
    correct, incorrect, accuracy = calculate_training_accuracy(predictions, labels)
    display_accuracy(correct, incorrect, accuracy)

if __name__ == "__main__":
    main()