import numpy as np
import scipy.stats as stats
import pandas as pd

# 1
mean = 2
std_dev = 30
n = 200
random_sample = np.random.normal(loc=mean, scale=std_dev, size=n)

t_statistic, p_value = stats.ttest_1samp(random_sample, 2.5)

print(f't-statistic = {t_statistic}, p_value = {p_value}')

alpha = 0.05
if p_value < alpha:
    print('Odrzucamy hipotezę zerową.')
else:
    print('Nie ma podstaw do odrzucenia hipotezy zerowej.')

# 2
df = pd.read_csv('napoje.csv', sep=';')
print(df.head())

mean_lech = 60500
mean_cola = 222000
mean_regional = 43500

t_stat_lech, p_value_lech = stats.ttest_1samp(df['lech'], mean_lech)
t_stat_cola, p_value_cola = stats.ttest_1samp(df['cola'], mean_cola)
t_stat_regional, p_value_regional = stats.ttest_1samp(df['regionalne'], mean_regional)

print(f'Test hipotezy dla Piwa Lech: t_statistic = {t_stat_lech}, p_value = {p_value_lech}')
print(f'Test hipotezy dla Coli: t_statistic = {t_stat_cola}, p_value = {p_value_cola}')
print(f'Test hipotezy dla Piwa Regionalnego: t_statistic = {t_stat_regional}, p_value = {p_value_regional}')

p_vals = [p_value_lech, p_value_cola, p_value_regional]
for p_val in p_vals:
    if p_val < alpha:
        print('Odrzucamy hipotezę zerową.')
    else:
        print('Nie ma podstaw do odrzucenia hipotezy zerowej.')

# 3
for column in df.columns[1:]:
    t_stat, p_value = stats.shapiro(df[column])
    print(f'Test normalności dla zmiennej {column}: t_statistic = {t_stat}, p_value = {p_value}')

    if p_value > alpha:
        print('Nie ma podstaw do odrzucenia hipotezy zerowej - rozkład normalny.')
    else:
        print('Odrzucamy hipotezę zerową - rozkład nie jest normalny.')
    print()

# 4
pairs = [('okocim', 'lech'), ('fanta ', 'regionalne'), ('cola', 'pepsi')]

for var1, var2 in pairs:
    data1 = df[var1]
    data2 = df[var2]

    t_stat, p_value = stats.ttest_rel(data1, data2)

    print(f'Test t-studenta dla par {var1} i {var2}: t_statistic = {t_stat}, p_value = {p_value}')
    if p_value > alpha:
        print('Nie ma podstaw do odrzucenia hipotezy zerowej - średnie są równe.')
    else:
        print('Odrzucamy hipotezę zerową - średnie nie są równe.')
    print()

# 5
pairs = [('okocim', 'lech'), ('żywiec', 'fanta '), ('regionalne', 'cola')]

for var1, var2 in pairs:
    data1 = df[var1]
    data2 = df[var2]

    stat, p_value = stats.levene(data1, data2)

    print(f'Test Levenea dla par {var1} i {var2}: t_statistic = {stat}, p_value = {p_value}')
    if p_value > alpha:
        print('Nie ma podstaw do odrzucenia hipotezy zerowej - wariancje są równe.')
    else:
        print('Odrzucamy hipotezę zerową - wariancje nie są równe.')
    print()

# 6
data_2001 = df[df['rok'] == 2001]['regionalne']
data_2015 = df[df['rok'] == 2015]['regionalne']

t_stat, p_value = stats.ttest_ind(data_2001, data_2015)

print(f'Test t-studenta dla piw regionalnych w latach 2001 i 2015: t_statistic = {t_stat}, p_value = {p_value}')
if p_value > alpha:
    print('Nie ma podstaw do odrzucenia hipotezy zerowej - średnie są równe.')
else:
    print('Odrzucamy hipotezę zerową - średnie nie są równe.')

# 7
df_2016 = df[df['rok'] == 2016]
df_po_reklamie = pd.read_csv('napoje_po_reklamie.csv', sep=';')

print(df_2016.head())
print(df_po_reklamie.head())

pairs = ['cola', 'fanta ', 'pepsi']

for var in pairs:
    data_2016 = df_2016[var]
    data_po_reklamie = df_po_reklamie[var]

    t_stat, p_value = stats.ttest_rel(data_2016, data_po_reklamie)

    print(f'Test t-studenta dla {var}: t_statistic = {t_stat}, p_value = {p_value}')
    if p_value > alpha:
        print('Nie ma podstaw do odrzucenia hipotezy zerowej - średnie są równe.')
    else:
        print('Odrzucamy hipotezę zerową - średnie nie są równe.')
    print()