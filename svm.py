import csv
import sklearn.svm

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

# Convert the training data into actual lists containing
# the curves, and the labels
def parse_training_data(data):
    # Parse the data into curves and labels
    curves = list(map(lambda c: c[:-1], data))
    labels = list(map(lambda c: c[-1], data))

    return curves, labels

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
    data = read_data("data\\TrainingData.txt")
    curves, labels = parse_training_data(data)
    classifier = train(curves, labels)
    predictions = predict(classifier, curves)
    correct, incorrect, accuracy = calculate_training_accuracy(predictions, labels)
    display_accuracy(correct, incorrect, accuracy)

if __name__ == "__main__":
    main()