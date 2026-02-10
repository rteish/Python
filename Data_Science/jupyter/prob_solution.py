
from scipy.stats import norm

# Calculate the probability of a random variable lying between -1 and 1 in a standard normal distribution
# P(-1 < Z < 1) = P(Z < 1) - P(Z < -1)
# For standard normal distribution, mean=0, std=1
prob = norm.cdf(1) - norm.cdf(-1)

print(f"Probability that a random variable lies between -1 and 1 in a standard normal distribution: {prob}")
