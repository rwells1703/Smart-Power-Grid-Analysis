import csv
import sklearn.svm

def read_data():
    with open("data\TrainingData.txt") as file:
        # Read the CSV file data
        reader = csv.reader(file)

        data = []
        # Store each line of the data into a list
        for row in reader:
            data.append([float(v) for v in row])

    return data

def main():
    # Read training data from files
    data = read_data()

    # Parse the data into curves and labels
    curves = list(map(lambda c: c[:-1], data))
    labels = list(map(lambda c: c[-1], data))

    # Fit the classifier to the data
    classifier = sklearn.svm.SVC()
    classifier.fit(curves, labels)
    print("Fitted")

    # Make predictions based upon training data
    predictions = classifier.predict(curves)
    print("Predicted")

    # Verify the predictions
    correct = 0
    i = 0
    while i < len(predictions):
        if predictions[i] == labels[i]:
            correct += 1
        i += 1

    print(f"Correct: {correct}")
    print(f"Incorrect: {len(predictions)-correct}")
    print(f"Accuracy: {correct/len(predictions)}")

if __name__ == "__main__":
    main()