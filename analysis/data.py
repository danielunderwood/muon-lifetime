"""
Module for getting and processing data
"""

from warnings import warn


def get_data(data_file='muon.dat', threshold=40000):
    """
    Reads the space-delimited data from the muon lifetime apparatus

    :param data_file: Data file to use. Defaults to file included in repo
    :param threshold: Threshold to trim data higher than to remove data points that lasted an entire cycle of the
                      apparatus timing
    :return: Integer array of data less than threshold
    """
    with open(data_file, 'r') as data:
        # Create array from data
        data_arr = [int(line.split(' ')[0]) for line in data]

        # Throw away events outside of 40us window
        return [datum for datum in data_arr if datum < threshold]


def get_bins(data, num_bins=10000):
    """
    Gets data bins for data

    :param data: Data to use for bins
    :param num_bins: Number of bins to create
    :return: Array of bins
    """

    # Round num_bins if it is not an integer
    if not isinstance(num_bins, int):
        warn("num_bins is not an integer. Rounding")
        num_bins = round(num_bins)

    range(min(data), max(data), (max(data) - min(data)) / num_bins)
