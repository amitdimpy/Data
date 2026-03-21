import seaborn as sns
import matplotlib.pyplot as plt
# Load a sample dataset
tips = sns.load_dataset("tips")

# Create a histogram of the 'total_bill' column
sns.histplot(data=tips, x="total_bill")
plt.title("Distribution of Total Bill Amounts")
plt.show()
sns.displot(data=tips)
plt.show()
sns.jointplot(data=tips)
plt.show()