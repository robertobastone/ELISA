############################## LIBRARIES
import matplotlib.pyplot as plt
import numpy as np
from lifelines.datasets import load_waltons
from lifelines import *

fig, ax = plt.subplots(1, 1, figsize=(13.5, 7.5))

df = load_waltons() # returns a Pandas DataFrame
T = df['T']
E = df['E']

print(df.to_string())


groups = df['group']
ix = (groups == 'miR-137')

kmf = KaplanMeierFitter().fit(T, E, label='group A')

kmf.fit(T[~ix], E[~ix], label='control')
ax = kmf.plot_survival_function(ci_show=False)
kmf.fit(T[ix], E[ix], label='miR-137')
ax = kmf.plot_survival_function(ax=ax, ci_show=False)

plt.savefig('elisa.png', dpi=400)