import csv
from matplotlib import pyplot as plt
import numpy as np
import scipy.signal as signal
from scipy.interpolate import interp1d

def read_curves():
    with open("data\TestingData.txt") as file:
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

    peaks = np.concatenate(([0], peaks, [len(curve)-1]))
    peak_heights = np.concatenate(([curve[0]], peak_heights, [curve[-1]]))

    return peaks, peak_heights

def find_troughs(curve):
    inverse_curve = np.multiply(curve, -1)

    troughs = signal.find_peaks(inverse_curve)[0]
    trough_heights = list(map(lambda i : curve[int(i)], troughs))

    troughs = np.concatenate(([0], troughs, [len(curve)-1]))
    trough_heights = np.concatenate(([curve[0]], trough_heights, [curve[-1]]))

    return troughs, trough_heights

def fit_curve_to_points(x, y):
    cubic_interpolation = interp1d(x, y, kind="nearest", fill_value="extrapolate")
    x_full = np.linspace(0, 23, 24)
    return x_full, cubic_interpolation(x_full)
    #coeffs = np.polynomial.Polynomial.fit(points_x, points_y, 9)
    #return coeffs.linspace(n=24, domain=[0,23])

def polynomial_approx_curve(curve):
    peaks, peak_heights = find_peaks(curve)
    troughs, trough_heights = find_troughs(curve)
    peaks_fitted_curve = fit_curve_to_points(peaks, peak_heights)
    troughs_fitted_curve = fit_curve_to_points(troughs, trough_heights)
    average_fitted_curve = np.add(peaks_fitted_curve, troughs_fitted_curve)/2

    plt.plot(range(len(curve)), curve)
    plt.scatter(peaks, peak_heights, c="#34c754")
    plt.scatter(troughs, trough_heights, c="#d93529")
    plt.plot(peaks_fitted_curve[0], peaks_fitted_curve[1])
    plt.plot(troughs_fitted_curve[0], troughs_fitted_curve[1])
    plt.plot(average_fitted_curve[0], average_fitted_curve[1])
    plt.show()

    return average_fitted_curve, (peaks, peak_heights, peaks_fitted_curve), (troughs, trough_heights, troughs_fitted_curve)

def empirical_mode_decomposition(curve, iterations):
    # List of intrinsic mode functions for the curve at each iteration
    imfs = []

    residue = curve

    i = 0
    while i < iterations:
        approximated_residue = polynomial_approx_curve(residue)[0][1]

        residue = residue - approximated_residue
        imfs.append(residue)

        i += 1
        
    return imfs

def main():
    curves = read_curves()

    imfs = empirical_mode_decomposition(curves[0], 50)
    for c in imfs:
        plt.plot(range(len(c)), c)
    plt.show()

def fit():
    curves = read_curves()
    c = curves[30]

    peaks = np.concatenate(([0], signal.find_peaks(c)[0], [len(c)-1]))
    peak_heights = list(map(lambda i : c[int(i)], peaks))

    coeffs = np.polynomial.Polynomial.fit(peaks, peak_heights, 4)
    linspace = coeffs.linspace(n=24, domain=[0,24])

    plt.plot(range(len(c)), c)
    plt.plot(linspace[0], linspace[1])
    plt.show()

if __name__ == "__main__":
    main()