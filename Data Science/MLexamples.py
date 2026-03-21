from sklearn.datasets import load_iris
from sklearn.datasets import fetch_20newsgroups
from sklearn.datasets import make_classification

iris = load_iris()
X = iris.data          # Feature matrix (150 samples, 4 features)
y = iris.target        # Target labels (species)
newsgroups = fetch_20newsgroups(subset='train')
X, y = make_classification(n_samples=100, n_features=5, n_classes=3, random_state=42)
print(iris.DESCR)      # Dataset description
#newsgroups = fetch_20newsgroups(subset='train')
print(len(newsgroups.data))  # Number of documents
print(newsgroups.target_names)  # List of categories
#X, y = make_classification(n_samples=100, n_features=5, n_classes=3, random_state=42)
print(X.shape, y.shape)
