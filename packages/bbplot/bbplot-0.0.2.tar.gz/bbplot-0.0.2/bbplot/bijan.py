import numpy as np
import pandas as pd
from scipy.stats import t
import scipy.stats as stats
import statsmodels.api as sm
from pandas import DataFrame
import matplotlib.pyplot as plt
from sklearn import preprocessing


def resid(residual):
    # creating dataframe and then standardizing and normalizing
    residuals = DataFrame(residual)
    residuals.reset_index(drop=True, inplace=True)
    # designing a 1 by 1 plot 
    fig, ((ax1)) = plt.subplots(1, 1)
    fig.set_figheight(6)
    fig.set_figwidth(15)
    # top left subplot
    y_mean = [np.mean(residual)] * len(residual)
    ax1.plot(residuals, color='b', label='Residual')
    ax1.plot(y_mean, label='Mean', linestyle='--', color='r')
    #     ax1.set_title("Residual for 'y'", loc = 'center')
    ax1.set(ylabel="Residual")
    legend = ax1.legend(loc='upper right')
    plt.savefig('residuals_1.jpg', dpi=300)
    plt.show()

    t_dist = abs(np.mean(residual)) / (np.std(residual, ddof=1) / np.sqrt(len(residual)))
    p_value = (1 - t.cdf(t_dist, len(residual) - 1, loc=0, scale=1)) * 2

    width = (np.std(residual, ddof=1) / np.sqrt(len(residual))) * t.ppf(0.975, len(residual) - 1, loc=0, scale=1)
    print('Mean of Residual:   ', np.mean(residual))
    print('S.D. of Residual:   ', np.std(residual, ddof=1))
    print(f'Half Width :         {width}   (degree of freedom = {len(residual) - 1}, Confidence Level = 0.95)')
    print('p-value :           ', "%.4f" % p_value)


def eplot(residual):
    # creating dataframe and then standardizing and normalizing
    residuals = DataFrame(residual)
    residuals.reset_index(drop=True, inplace=True)
    mean = residuals.mean()
    std = residuals.std()
    residuals_std = (residuals - mean) / std
    rng = (0, 1)
    scaler = preprocessing.MinMaxScaler(feature_range=(rng[0], rng[1]))
    normed = scaler.fit_transform(np.array(residuals).reshape(-1, 1))
    residuals_norm = [round(i[0], 2) for i in normed]
    # designing a 2 by 2 plot 
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    fig.set_figheight(10)
    fig.set_figwidth(15)
    # top left subplot
    ax1.plot(residuals_std, color='b')
    #     ax1.set_title("Standard Residual for 'y'", loc = 'center')
    ax1.set(ylabel="Standard Residual")
    # top right subplot
    ax = residuals_std.plot(kind='hist', density=True, color='b', ec='w', ax=ax2)
    residuals_std.plot(kind='kde', ax=ax2, color='r')
    ax2.set_xlim(-4, 4)
    ax2.set_title("Histogram Plus Estimated Density", loc='center')
    ax2.get_legend().remove()
    # bottom left subplot
    stats.probplot(residuals_norm, dist="norm", plot=ax3)
    ax3.set_title("Normal Q-Q plot", loc='center')
    # bottom right subplot
    sm.graphics.tsa.plot_acf(residuals_std, color='b', ax=ax4)
    plt.savefig('residuals_2.jpg', dpi=300)
    plt.show()


def pval(residual):
    t_dist = abs(np.mean(residual)) / (np.std(residual, ddof=1) / np.sqrt(len(residual)))
    p_value = (1 - t.cdf(t_dist, len(residual) - 1, loc=0, scale=1)) * 2
    print('p-value :', "%.4f" % p_value)