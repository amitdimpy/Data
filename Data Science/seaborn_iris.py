import seaborn as sns
import matplotlib.pyplot as plt
data = sns.load_dataset("iris")

sns.lineplot(x="sepal_length", y="sepal_width", data=data) 
plt.show()
sns.displot(data=data, kind='ecdf')
plt.show()
sns.jointplot(data=data, kind='kde')
plt.show()