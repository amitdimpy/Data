import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

sns1 = sns.get_dataset_names()
print (sns1)
data = sns.load_dataset('brain_networks')
print(data)
graph = sns.FacetGrid(data,row='distance',col='year',height = 3, hue = 'mass', aspect=1.2)
graph.map (sns.histplot,'distance', 'year')
graph.add_legend()
plt.show()