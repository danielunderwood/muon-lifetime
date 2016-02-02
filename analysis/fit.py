import matplotlib

matplotlib.use('TkAgg')

from data import get_data
import matplotlib.pylab as plt
import numpy
from scipy.optimize import curve_fit




def fit_model(t, N0, l, B):
    """
    Model to fit the data to. Use for scipy.optimize.curve_fit

    :param t: Independent variable representing decay time
    :param N0: Amplitude of exponential (y-intercept)
    :param l: Decay constant lambda. Inverse of mean lifetime tau
    :param B: Constant factor added to account for background
    :return: Model evaluated with parameters
    """
    return N0 * l * numpy.exp(-l * t) + B

# Get data
data = get_data()

# Bin data
hist = numpy.histogram(data, bins=30)


# Bin counts
y = hist[0]

# Gaussian errors
err = numpy.sqrt(y)

# TODO: Change to bin midpoints
# Bin edges
x = hist[1][1:]

# Fit model and print parameters
params, pconv = curve_fit(fit_model, ydata=y, xdata=x, p0=[6500, 10**-6, 0], sigma=y)
sigma = numpy.sqrt(numpy.diag(pconv))
print('N0: ' + str(params[0]))
print('lambda: ' + str(params[1]))
print('B: ' + str(params[2]))
print('Sigma: ' + str(sigma))

# Generate points for plotting fit
x2 = range(int(min(x)), int(max(x)), int(max(x) - min(x)) / 1000)
y2 = [fit_model(t, params[0], params[1], params[2]) for t in x2]

# Plot data and fit
plt.errorbar(x, y, yerr=err, fmt='o')
plt.plot(x2, y2, linewidth=1, linestyle='--', c='red')
plt.xlim(min(x), max(x))
plt.xlabel('Time (ns)')
plt.ylabel('Muon Count')
plt.show()
