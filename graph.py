import csv
from matplotlib import pyplot as plt
import numpy as np
import scipy.signal as signal

def read_curves():
    with open("data\TestingData.csv") as file:
        # Read the CSV file data
        reader = csv.reader(file)

        curves = []
        # Store each line of the data into a list of curves
        for row in reader:
            curves.append([float(v) for v in row])

    return curves

def save_curve_images(curves):
    for i, c in enumerate(curves):
        plt.plot(range(len(c)), c)
        plt.savefig("figures\\curve{number}.jpg".format(number=i+1), format="jpg")
        plt.close()

def find_peaks(curve):
    peaks = signal.find_peaks(curve)[0]
    peak_heights = list(map(lambda i : curve[int(i)], peaks))

    return peaks, peak_heights

def find_troughs(curve):
    troughs = signal.find_peaks(np.multiply(curve, -1))[0]
    trough_heights = list(map(lambda i : curve[int(i)], troughs))

    return troughs, trough_heights

def fit_curve_to_points(points_x, points_y):
    coeffs = np.polynomial.Polynomial.fit(points_x, points_y, 3)
    return coeffs.linspace(n=24, domain=[0,24])

def polynomial_approx_curve(curve):
    peaks, peak_heights = find_peaks(curve)
    troughs, trough_heights = find_troughs(curve)
    peaks_fitted_curve = fit_curve_to_points(peaks, peak_heights)
    troughs_fitted_curve = fit_curve_to_points(troughs, trough_heights)
    average_fitted_curve = np.add(peaks_fitted_curve, troughs_fitted_curve)/2

    return average_fitted_curve, (peaks, peak_heights, peaks_fitted_curve), (troughs, trough_heights, troughs_fitted_curve)

def main():
    curves = read_curves()

    average_fitted_curve, (peaks, peak_heights, peaks_fitted_curve), (troughs, trough_heights, troughs_fitted_curve) = polynomial_approx_curve(curves[0])

    plt.plot(range(len(curves[0])), curves[0])
    plt.scatter(peaks, peak_heights, c="#34c754")
    plt.scatter(troughs, trough_heights, c="#d93529")
    plt.plot(peaks_fitted_curve[0], peaks_fitted_curve[1])
    plt.plot(troughs_fitted_curve[0], troughs_fitted_curve[1])
    plt.plot(average_fitted_curve[0], average_fitted_curve[1])
    plt.show()

if __name__ == "__main__":
    main()