import csv
from matplotlib import pyplot as plt
import numpy as np

with open("data\TestingData.csv") as file:
    # Read the CSV file data
    reader = csv.reader(file)

    curves = []
    # Store each line of the data into a list of curves
    for row in reader:
        curves.append([float(v) for v in row])
    
for i, c in enumerate(curves):
    plt.plot(range(len(c)), c)
    plt.savefig("figures\\curve{number}.jpg".format(number=i+1), format="jpg")
    plt.close()