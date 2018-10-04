import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from numpy import genfromtxt
import os
from pandas import read_csv

u = 10
df = read_csv('fire.csv')
x = np.array(df[df.Loss > u]['Loss'] - u)

def gdp_loglikelihood(p, y):

    xi, sigma = p

    if(xi <= 0 or sigma <= 0):
        return 1e8

    n = len(y)
    l = -n * np.log(sigma) - (1 + 1/xi)*np.sum(np.log(1 + xi * y / sigma))

    return -l

#y = x
x0 = np.array([1, 1])
#res = minimize(gdp_loglikelihood, x0, method='nelder-mead', options={'xtol': 1e-8, 'disp': True}, args=(x))
res = minimize(gdp_loglikelihood, x0, method='BFGS', options={ 'maxiter': 10000}, args=(x))
print(gdp_loglikelihood(np.array([0.4967484, 6.9761298]), x))
print(gdp_loglikelihood(np.array(res.x), x))
print(res.x)

from mpl_toolkits.mplot3d import Axes3D

def plot_joint_poisson(y):
    m = 100
    xi_values = np.arange(0.01, 5.01, (5.01-0.01)/m)
    sigma_values = np.arange(0.01, 10.01, (10.01-0.01)/m)

    # Create coordinate points of X and Y
    X, Y = np.meshgrid(xi_values, sigma_values)

    # Multiply distributions together
    Z = a = np.zeros(shape=(len(xi_values),len(sigma_values)))

    for i in range(0, len(xi_values) - 1):
        for j in range(0, len(sigma_values) - 1):
                a = X[i,j]
                b = Y[i,j]
                param = np.array([a, b])
                Z[i,j] =  gdp_loglikelihood(param, y)

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z.T, cmap='terrain', alpha=0.6)
    ax.scatter(X, Y, Z.T, color='black', alpha=0.5, linewidths=1)
    ax.set(xlabel='$y_1$', ylabel='$y_2$')
    ax.set_zlabel('$f(y_1, y_2)$', labelpad=10)
    plt.show()

plot_joint_poisson(x)
