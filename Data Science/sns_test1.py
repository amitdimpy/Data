import seaborn as sns
import matplotlib.pyplot as plt

# Load a sample dataset
tips = sns.load_dataset("tips")
print (tips)

# Create a FacetGrid with 'time' in columns and 'sex' in rows, and 'smoker' as hue
g = sns.FacetGrid(tips, col="time", row="sex", hue="smoker", height=3, aspect=1.2)

# Map a plotting function (e.g., scatterplot) to the grid
g.map(sns.scatterplot, "total_bill", "tip")

# Add a legend
g.add_legend()

plt.show()