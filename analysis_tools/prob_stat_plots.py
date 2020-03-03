import numpy as np
from matplotlib import pyplot as plt

def make_histogram(time_series_input, normal_pdf_overlay=True, density_values_y_axis = True):
    """
    :param time_series: a pandas.Series of the time-series data from which to create a histogram
    Example use case: If I know that my input data is normally distributed (visually meaning a histogram  with:
    1) symmetry around the mean/avg/estimated value and 2) a bell-shaped curve) then I can make "predictions"
    about my input data w/ a certain "confidence" (level).
    68-98-99.7 Rule:
    68% of data is within 1 std (standard deviation) of the mean
    95% of data is within 2 std (standard deviation) of the mean
    99.7% of data is within 3 std (standard deviation) of the mean
    Wikipedia: "These numerical values "68%, 95%, 99.7%" come from the cumulative distribution function of the normal distribution."
    Medium (Michael Galarnyk): "To be able to understand where the percentages come from, it is important to know about the probability density function (PDF).
    A PDF is used to specify the probability of the random variable falling within a particular range of values, as opposed to taking on any one value."
    Example math: X_avg +(or)- 2*(std/sqrt(n)) is approx. a 95% confidence interval when X_avg is the average of a sample of size n
    :return:
    """
    std = time_series_input.std()
    mean = time_series_input.mean()
    if normal_pdf_overlay is True:
        count, bins, ignored = plt.hist(time_series_input, 100, density=density_values_y_axis)
        # computing the normal pdf values and plotting
        plt.plot(bins, 1 / (std * np.sqrt(2 * np.pi)) * np.exp(- (bins - mean) ** 2 / (2 * std ** 2)), linewidth=2, color='r')
        plt.ylabel(r'Probability Density', fontsize = 10)
        plt.xlabel(r'Bins', fontsize = 10)
        plt.show()
    else:
        plt.hist(time_series_input, 100, density=density_values_y_axis)
        plt.ylabel(r'Number of Data Points per Bin', fontsize=10)
        plt.xlabel(r'Bins', fontsize=10)
        plt.show()


# Make a PDF for the normal distribution a function
def normalProbabilityDensity(x):
    constant = 1.0 / np.sqrt(2*np.pi)
    return(constant * np.exp((-x**2) / 2.0) )



if __name__ == "__main__":
    pass

