import pandas as pd
import scipy.stats as scs
import numpy as np
import matplotlib.pyplot as plt

# 1
data = pd.DataFrame({"Wartość" : [1,2,3,4,5,6], "Prawdopodobieństwo": [1/6, 1/6, 1/6, 1/6, 1/6, 1/6]})
print(data.describe())

n = 100
p = 0.3
data_bernoulli = scs.bernoulli.rvs(p, size=n)
mean, var, skew, kurt = scs.bernoulli.stats(p, moments='mvsk')
print('Bernoulliego: ', 'średnia:', mean, ' wariancja:', var, ' skośność:', skew, ' kurtoza:', kurt)

n_dwumian = 1
data_binom = scs.binom.rvs(n_dwumian, p, size=n)
mean, var, skew, kurt = scs.binom.stats(n_dwumian, p, moments='mvsk')
print('Dwumianowy: ', 'średnia:', mean, ' wariancja:', var, ' skośność:', skew, ' kurtoza:', kurt)

lambda_poisson = 0.3
data_poisson = scs.poisson.rvs(lambda_poisson, size=n)
mean, var, skew, kurt = scs.poisson.stats(lambda_poisson, moments='mvsk')
print('Poissona: ', 'średnia:', mean, ' wariancja:', var, ' skośność:', skew, ' kurtoza:', kurt)

# 2
p_bernoulli = 0.5
n_binom = 10
p_binom = 0.3
lambda_poisson = 3

x_bernoulli = [0, 1]
x_binom = np.arange(0, n_binom + 1)
x_poisson = np.arange(0, 2 * lambda_poisson + 1)

prob_bernoulli = scs.bernoulli.pmf(x_bernoulli, p_bernoulli)
prob_binom = scs.binom.pmf(x_binom, n_binom, p_binom)
prob_poisson = scs.poisson.pmf(x_poisson, lambda_poisson)

plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.bar(x_bernoulli, prob_bernoulli, align='center', alpha=0.7)
plt.title('Rozkład prawdopodobieństwa - Bernoulli')
plt.xlabel('Wartość')
plt.ylabel('Prawdopodobieństwo')

plt.subplot(1, 3, 2)
plt.bar(x_binom, prob_binom, align='center', alpha=0.7)
plt.title('Rozkład prawdopodobieństwa - Dwumianowy')
plt.xlabel('Wartość')
plt.ylabel('Prawdopodobieństwo')

plt.subplot(1, 3, 3)
plt.bar(x_poisson, prob_poisson, align='center', alpha=0.7)
plt.title('Rozkład prawdopodobieństwa - Poissona')
plt.xlabel('Wartość')
plt.ylabel('Prawdopodobieństwo')

plt.tight_layout()
plt.show()

# 3
n_binom = 20
p_binom = 0.4
x_binom = np.arange(0, n_binom + 1)
prob_binom = scs.binom.pmf(x_binom, n_binom, p_binom)
suma_prawdopodobienstw = np.sum(prob_binom)

plt.bar(x_binom, prob_binom, align='center', alpha=0.7)
plt.title('Rozkład prawdopodobieństwa - Dwumianowy')
plt.xlabel('Wartość k')
plt.ylabel('Prawdopodobieństwo')

plt.show()

print(f'Suma prawdopodobieństw: {suma_prawdopodobienstw}')

# 4
m = 0
std_dev = 2

data = np.random.normal(loc=m, scale=std_dev, size=n)

mean = np.mean(data)
var = np.var(data)
stddev = np.std(data)
skewness = scs.skew(data)
kurtosis = scs.kurtosis(data)

print("Statystyki opisowe dla 100 danych:")
print(f"Średnia: {mean} (teoretyczna: {m})")
print(f"Wariancja: {var} (teoretyczna: {std_dev**2})")
print(f"Odchylenie standardowe: {stddev} (teoretyczne: {std_dev})")
print(f"Skośność: {skewness} (teoretyczna: 0)")
print(f"Kurtoza: {kurtosis} (teoretyczna: 0)")

n = 1000
new_data = np.random.normal(loc=mean, scale=std_dev, size=n)

new_mean = np.mean(new_data)
new_var = np.var(new_data, ddof=1)
new_stddev = np.std(new_data, ddof=1)
new_skewness = scs.skew(new_data)
new_kurtosis = scs.kurtosis(new_data)

print("\nStatystyki opisowe dla 1000 danych:")
print(f"Nowa średnia: {new_mean} (teoretyczna: {m})")
print(f"Nowa wariancja: {new_var} (teoretyczna: {std_dev**2})")
print(f"Nowe odchylenie standardowe: {new_stddev} (teoretyczne: {std_dev})")
print(f"Nowa skośność: {new_skewness} (teoretyczna: 0)")
print(f"Nowa kurtoza: {new_kurtosis} (teoretyczna: 0)")

# 5
mean = 1
std_dev = 2
mean2 = -1
std_dev2 = 0.5

data = np.random.normal(loc=mean, scale=std_dev, size=1000)
x = np.linspace(min(data), max(data), 1000)
data2= scs.norm.pdf(x, loc=mean2, scale=std_dev2)

plt.figure(figsize=(10, 6))

plt.hist(data, bins=30, density=True, alpha=0.7, label='Rozkład normalny')
plt.plot(x, scs.norm.pdf(x, loc=mean, scale=std_dev), 'r--', label='Rozkład standardowy')
plt.plot(x, data2, 'g-', label='Wykres gęstości')

plt.xlabel('Wartość')
plt.ylabel('Gęstość prawdopodobieństwa')
plt.legend()

plt.show()