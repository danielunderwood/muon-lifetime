import matplotlib

matplotlib.use('TkAgg')

from data import get_data
import matplotlib.pylab as plt
import numpy
import os
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

if __name__ == '__main__':

    DATA_DIR = os.path.realpath('../resources')
    DATA_FILE_PATH = os.path.join(DATA_DIR, 'muon.dat')
    PLOT_SAVE_PATH = os.path.join(DATA_DIR, 'muon-plot.pdf')

    # Get data
    data = get_data(DATA_FILE_PATH)

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
    params, pconv = curve_fit(fit_model, ydata=y, xdata=x, p0=[6500, 10**-6, 0], sigma=err)
    sigma = numpy.sqrt(numpy.diag(pconv))

    # Value, plus, minus deviation tuples
    N0 = (params[0], sigma[0], sigma[0])
    l = (params[1], sigma[1], sigma[1])
    B = (params[2], sigma[2], sigma[2])

    # Lifetime calculation from 1/lambda
    tau = 1/l[0]
    tau_min = 1 / (l[0] + l[1])
    tau_max = 1 / (l[0] - l[2])
    dev_min = tau - tau_min
    dev_max = tau_max - tau

    tau = (tau, dev_min, dev_max)

    # Calculate Reduced chi squared
    chi_squared = numpy.sum((fit_model(x, N0[0], l[0], B[0]) - y) ** 2
            / err ** 2)
    degrees_of_freedom = len(y) - len(params) - 1
    reduced_chi_squared = chi_squared / degrees_of_freedom

    print('N0: %E +(-) %E(%E)' % N0)
    print('lambda: %E +(-) %E(%E)' % l)
    print('tau: %E +(-) %E(%E)' % tau)
    print('B: %E +(-) %E(%E)' % B)
    print('Chi Squared: %f' % chi_squared)
    print('Degrees of Freedom: %d' % degrees_of_freedom)
    print('Reduced Chi Squared: %f' % reduced_chi_squared)

    # Generate points for plotting fit
    x2 = range(int(min(x)), int(max(x)), int(max(x) - min(x)) / 1000)
    y2 = [fit_model(t, params[0], params[1], params[2]) for t in x2]

    # Plot data and fit
    plt.ion()
    collected_data = plt.errorbar(x, y, yerr=err, fmt='o', label='Muon Decay Events')
    fit_line = plt.plot(x2, y2, linewidth=1, linestyle='--', c='red', label='Fitted Curve')
    plt.xlim(min(x), max(x))
    plt.xlabel('Time (ns)')
    plt.ylabel('Muon Count')
    plt.legend()
    plt.show()
    plt.savefig(PLOT_SAVE_PATH)
