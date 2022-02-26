# ft.py

from sklearn import datasets
from myConvexHull import myConvexHull 
import matplotlib.pyplot as plt
data = datasets.load_iris()
data.data = data.data[:,:2]

print(data.data)
ch = myConvexHull(data.data.tolist())
print(ch.vertices)
print(ch.points)
print(ch.contained)
print(ch.lines)
ch.visualize()

data2 = [[0,1], [2,4], [4,4], [0,0], [1,1], [3,1], [3,2]]
'''
ch2 = myConvexHull(data2)
print(ch2.vertices)
print(ch2.points)
print(ch2.contained)
print(ch2.lines)
ch2.visualize() '''

data3 = [[5.1,3.5], [4.9,3.0], [4.7,3.2], [4.6,3.1], [5.0,3.6]] 
'''
ch3 = myConvexHull(data3)
print(ch3.vertices)
print(ch3.points)
print(ch3.contained)
print(ch3.lines)

ch3.visualize()'''