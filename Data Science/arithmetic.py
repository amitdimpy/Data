import numpy as np

a = np.array([1,2,3,40,5,6])
print(f"Max of a: {a.max()}")
b = np.array([[1,2,70,5,6],[10,50,20,35,5]])
print(f"Max Rows Output is: {b.max(axis=1)}") #Rows
print(f"Max Columns Output is: {b.max(axis=0)}") #Columns
print(f"Max Output of b is: {b.max()}")
print(f"Min Output of b is: {b.min()}")
print(f"Min Rows Output in b is: {b.min(axis=1)}") #Rows
print(f"Min Columns Output in b is: {b.min(axis=0)}") #Columns
print(f"Sum of a: {a.sum()}")
print(f"Sum of rows b: {b.sum(axis=1)}") #Rows
print(f"Sum of columns b: {b.sum(axis=0)}") #Columns
print(f"Sum of b: {b.sum()}")
c = ([[100,400,1000,900,1600],[25,36,49,81,16]])
d = np.array([10,20,30,40,50,60])
print(f"Sqrt of c: {np.sqrt(c)}")
print(f"Sqrt of b: {np.sqrt(b)}")
print(f"Standard Deviation of b: {np.std(b)}")
print(f"Standard Deviation of c: {np.std(c)}")
print(f"Vertical Stack of a and d is : {np.vstack((a,d))}")
print(f"Horizontal Stack of b and c is : {np.hstack((b,c))}")
print(f"Ravel Falttened Array of c is: {np.ravel((c))}") #Flatten array