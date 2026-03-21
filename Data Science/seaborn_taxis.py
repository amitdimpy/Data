import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
data = sns.load_dataset('taxis')
sns.lineplot(data=data)
plt.show()
sns.scatterplot(data=data)
plt.show()
sns.displot(data=data,x="passengers",y="fare", kind='kde')
plt.show()
sns.histplot(data=data,x="passengers",y="fare")
plt.show()