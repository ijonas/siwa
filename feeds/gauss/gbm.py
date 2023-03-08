import numpy as np
import matplotlib.pyplot as plt
import random

def geometric_brownian_motion(S0, mu, sigma, T, N, seed=None):
    """
    Generate geometric Brownian motion using the Black-Scholes-Merton model.

    Args:
    S0 (float): initial stock price
    mu (float): expected return
    sigma (float): volatility
    T (float): time horizon (in years)
    N (int): number of time steps
    seed (int): random seed for reproducibility (optional)

    Returns:
    (np.ndarray): an array of length N+1 representing the simulated stock prices.
    """

    dt = T / N
    t = np.linspace(0, T, N+1)
    np.random.seed(seed)
    W = np.random.standard_normal(size=N+1)
    W[0] = 0
    W = np.cumsum(W)*np.sqrt(dt)
    drift = (mu - 0.5*sigma**2) * t
    diffusion = sigma * W
    S = S0*np.exp(drift + diffusion)

    return S

# Example usage
S0 = 100  # initial stock price
mu = 0.0  # expected return
sigma = 0.2  # volatility
T = .01  # time horizon (in years)
N = 50  # number of time steps (daily data)
seed = 1234  # random seed for reproducibility

Sl = [geometric_brownian_motion(S0, mu, sigma, T, N, seed=seed)]
for i in range(100):
    Sl.append(geometric_brownian_motion(Sl[i][-1], random.uniform(-0.5, 0.5),
              sigma, T, N, seed=seed))

S = np.concatenate(Sl)

# Plot the results
plt.plot(S)
plt.xlabel('Time step')
plt.ylabel('Stock price')
plt.title('Geometric Brownian Motion')
plt.show()
