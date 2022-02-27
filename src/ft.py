# ft.py

from sklearn import datasets
from myConvexHull import myConvexHull 
import matplotlib.pyplot as plt
import pandas as pd
data = datasets.load_iris()

#ch = myConvexHull(data.data.tolist())
#ch.visualize()

df = pd.DataFrame(data.data, columns=data.feature_names) 
df['Target'] = pd.DataFrame(data.target) 

bucket = df[df['Target'] == 0]
bucket = bucket.iloc[:,[0,1]].values.tolist()

'''
plt.figure(figsize = (10, 6))
for point in bucket :
    plt.plot(point[0], point[1], 'bo')
plt.show()'''


ch = myConvexHull(bucket)
ch.visualize()

'''
plt.figure(figsize = (10, 6))
colors = ['b','r','g']
plt.title('Petal Width vs Petal Length')
plt.xlabel(data.feature_names[0])
plt.ylabel(data.feature_names[1])

for i in range(len(data.target_names)):
    bucket = df[df['Target'] == i]
    bucket = bucket.iloc[:,[0,1]].values.tolist()
    print(bucket)
    hull = myConvexHull(bucket) #bagian ini diganti dengan hasil implementasi ConvexHull Divide & Conquer
    #hull.visualize()
    #plt.scatter(bucket[:][0], bucket[:][1], label=data.target_names[i])
    #for line in hull.lines:
        #plt.plot([hull.points[line[0]][0], hull.points[line[1]][0]], [hull.points[line[0]][1], hull.points[line[1]][1]], colors[i])
plt.legend()
plt.show()'''

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

ch3.visualize() '''