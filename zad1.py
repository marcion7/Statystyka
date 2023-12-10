import pandas as pd
from statistics import mean, median_high, median_low, mode, variance, stdev
import scipy.stats as st
import pandas.plotting as pdp
import matplotlib.pyplot as plt

data = pd.read_csv('MDR_RR_TB_burden_estimates_2023-12-05.csv')
print(data.describe())

wzrost = pd.read_csv('Wzrost.csv')

print("Median High: ", median_high(wzrost))
print("Median Low: ", median_low(wzrost))
print("Mode: ", mode(wzrost))
print("Variance: ", variance(wzrost.columns.astype(float)))
print("Stdev: ", stdev(wzrost.columns.astype(float)))

game_sales = pd.read_csv('video_game_sales.csv')
game_sales = game_sales[['Total_Sales']]

print("Kurtosis: ", st.kurtosis(game_sales))
print("Skewness: " , st.skew(game_sales))
print("Describe: ", st.describe(game_sales))
print("Mode: ", st.mode(game_sales))
print("RankData: ", st.rankdata(game_sales))
print("ZScore: ", st.zscore(game_sales))

brain = pd.read_csv('brain_size.csv', delimiter=';')

print("Średnia VIQ: ", mean(brain['VIQ']))
print("Ilość mężczyzn: ", brain['Gender'].value_counts()['Male'],"Ilość kobiet: ", brain['Gender'].value_counts()['Female'])

pdp.scatter_matrix(brain[['VIQ']])
pdp.scatter_matrix(brain[['PIQ']])
pdp.scatter_matrix(brain[['FSIQ']])
plt.show()

brain_female = brain[brain['Gender'] == "Female"]
    
pdp.scatter_matrix(brain_female[['VIQ']])
pdp.scatter_matrix(brain_female[['PIQ']])
pdp.scatter_matrix(brain_female[['FSIQ']])
plt.show()


