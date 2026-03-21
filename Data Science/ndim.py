# For checking number of dimension of array, Itemsize and Array size
import numpy as np

a = np.array(42)
print(f"Array 'a':{a}, andim: {a.ndim}, Itemsize: {a.itemsize}, Size: {a.size}, Arr_size: {a.size * a.itemsize}")
b = np.array([1,2,3,4,5,6])
print (f"Array 'b':{b}, bndim: {b.ndim}, Itemsize: {b.itemsize}, Size: {b.size}, Arr_size: {b.size * b.itemsize}")
c = np.array([[(1,2,3),(4,5,6),(7,8,9)]])
print(f"Array 'c':{c}, cndim: {c.ndim}, Itemsize: {c.itemsize}, Size: {c.size}, Arr_size: {c.size * c.itemsize}")
d = np.array([[(1,2,3,4),(4,5,6,7),(8,9,10,11),(12,13,14,15)]])
print(f"Array 'd':{d}, dndim: {d.ndim}, Itemsize: {d.itemsize}, Size: {d.size}, Arr_size: {d.size * d.itemsize}")