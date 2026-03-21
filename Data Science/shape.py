# To get shape of arrays and reshape of array
# Reshape converts range into array size specified
import numpy as np

a = np.array([1,2,3])
b = np.array([(1,2,3,4),(5,6,7,8)])
print(f"Shape of array a (rows,column): {a.shape}")
print(f"Shape of array b (rows,column): {b.shape}")
c = np.arange(12)  # For reshape
d = c.reshape(3,4)
print(f"Reshape1: {d}")
e = c.reshape(2,6)
print(f"Reshape2: {e}")
f = c.reshape(6,2)
print(f"Reshape : {f}")