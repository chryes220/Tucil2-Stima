# ft.py

from myConvexHull import myConvexHull

#create a DataFrame 
import numpy as np
list = [[1,1], [2,2], [4,4], [0,0], [1,2], [3,1], [3,3]]

ch = myConvexHull(list)
print(ch.points)
print(ch.vertices)
print(ch.lines)
print(ch.contained)