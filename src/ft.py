# ft.py

from sklearn import datasets
from myConvexHull import myConvexHull 
import matplotlib.pyplot as plt
import pandas as pd

data = datasets.load_wine()

#ch = myConvexHull(data.data.tolist())
#ch.visualize()

df = pd.DataFrame(data.data, columns=data.feature_names) 
df['Target'] = pd.DataFrame(data.target) 

plt.figure(figsize = (10, 6))
colors = ['b','r','g']
plt.title('Alcohol vs Malic Acid')
plt.xlabel(data.feature_names[0])
plt.ylabel(data.feature_names[1])

for i in range(len(data.target_names)):
    bucket = df[df['Target'] == i]
    bucket = bucket.iloc[:,[0,1]].values
    hull = myConvexHull(bucket) #bagian ini diganti dengan hasil implementasi ConvexHull Divide & Conquer
    plt.scatter(bucket[:, 0], bucket[:, 1], label=data.target_names[i])
    for line in hull.lines:
        plt.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], colors[i])
plt.legend()
plt.show()
