# To slice the array
import numpy as np

a = np.array([10,20,30,40,50,60,70,80,90,100]) # 1D array slicing
print(a[2:6])  # print from 2 to 6
print(a[0:5:2]) # print from 0 to every 2nd value till 5
print(a[1:8]) # print from 1 to 8
print(a[::4]) # print from 0 to end every 4th value
print(a[::-1]) # print value in reverse

b = np.array([[1,2,3,4],[5,6,7,8],[10,11,12,13]])
print(b[0:1,1:3])
print(b[:,1]) # print all rows first column
print(b[2,:]) # print 2nd row all columns
mask = b > 10
print(mask) # Values less than 10 are False and greater are True
print(b[b > 12]) # Output value greater than 12
print(b[b < 5]) # Output value less than 5
print(b[:,1] >= 6) # Output all rows first column which are >= 6