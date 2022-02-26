# myConvexHull.py

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

class myConvexHull:
    points = [] # berisi point (point didefinisikan sebagai array of float dengan panjang 2 elemen)
    vertices = [] # berisi indeks dari point dalam points yang membentuk convex hull
    lines = [] # berisi indeks dari point-point yang membentuk garis convex hull (didefinisikan sebagai array of integer dengan panjang 2 element)
    outer = [] # berisi indeks dari dua point terluar, dengan points[outer[0]][0] < points[outer[1]][0]
    contained = set() # set yang berisi indeks dari point-point yang sudah berada di dalam area
    data = []
    df = []
    count_contained = 0

    def __init__(self, data) :
        # arr_of_points bertipe Bunch, namun diubah dan diolah dalam bentuk array of points
        '''
        self.data = data # Bunch masih disimpan
        self.df = pd.DataFrame(data.data, columns=data.feature_names) # juga disimpan dalam bentuk data frame
        self.points = data.data[:,:2].tolist() '''
        self.points = data

        #print("points : ", self.points)
        #print([4.6, 3.1] in self.points)

        self.outer = self.find_outer_points()

        # since outer points surely create the convex hull
        self.vertices.append(self.outer[0])
        self.vertices.append(self.outer[1])
        self.lines.append([self.outer[0], self.outer[1]])
        self.contained.add(self.outer[0])
        self.contained.add(self.outer[1])

        init_reg = self.points.copy()
        left_point = self.points[self.outer[0]]
        right_point = self.points[self.outer[1]]
        init_reg.pop(init_reg.index(left_point))
        init_reg.pop(init_reg.index(right_point))

        self.findConvexHull(left_point, right_point, init_reg)

    def find_outer_points (self) :
        # mencari point-point dengan nilai absis terendah dan tertinggi
        # mengembalikan array dua elemen dalam bentuk [indeks point terkiri, indeks point terkanan]
        res = [-1,-1]
        min_x = 999999
        max_x = -1

        for i in range (len(self.points)) :
            if self.points[i][0] < min_x :
                min_x = self.points[i][0]
                res[0] = i
            if self.points[i][0] > max_x :
                max_x = self.points[i][0]
                res[1] = i
        return res

    def determinant(self, point_line1, point_line2, point) :
        # mencari nilai determinan untuk menentukan di daerah mana sebuah point berada
        # point_line1, point_line2, point : point
        # point_line1 dan point_line2 adalah ujung-ujung dari garis pembatas daerah
        det = (point_line1[0] * point_line2[1]) + (point[0] * point_line1[1]) + (point_line2[0] * point[1]) - (point[0] * point_line2[1]) - (point_line2[0] * point_line1[1]) - (point_line1[0] * point[1])
        return det

    def find_furthest_idx(self, point_line1, point_line2, region) :
        # mengembalikan indeks dari titik terjauh dengan garis dan memasukkan indeks yang bukan merupakan paling jauh ke dalam contained
        # dipastikan len(region) > 1
        furthest = -1
        idx = -1
        a = point_line1[1] - point_line2[1]
        b = point_line2[0] - point_line1[0]
        c = (point_line1[0] * point_line2[1]) - (point_line2[0] * point_line1[1])

        for point in region :
            denom = math.sqrt(a**2 + b**2)
            if (denom != 0) :
                dist = abs(((a * point[0]) + (b * point[1]) + c)/denom)
                if (dist > furthest) :
                    furthest = dist
                    idx = self.points.index(point)
        return idx

    def is_contained(self, p1, p2, p3, point) :
        # menggunakan barycentric coordinate
        # referensi : https://mathworld.wolfram.com/TriangleInterior.html#:~:text=The%20simplest%20way%20to%20determine,it%20lies%20outside%20the%20triangle.
        
        denom = (p2[1] - p3[1])*(p1[0] - p3[0]) + (p3[0] - p2[0])*(p1[1] - p3[1])
        if (denom != 0) :
            a = ((p2[1] - p3[1])*(point[0] - p3[0]) + (p3[0] - p2[0])*(point[1] - p3[1])) / denom
            b = ((p3[1] - p1[1])*(point[0] - p3[0]) + (p1[0] - p3[0])*(point[1] - p3[1])) / denom
            c = 1 - a - b
            return ((0 <= a <= 1) and (0 <= b <= 1) and (0 <= c <= 1))
        else :
            return False
    
    def update_contained(self, p1, p2, p3, region) :
        for point in region :
            if (self.is_contained(p1, p2, p3, point)) :
                self.contained.add(self.points.index(point))

    def findConvexHull (self, point_line1, point_line2, region) :
        # region : array of points
        # point_line1, point_line2 : point

        pl1_idx = self.points.index((point_line1))
        pl2_idx = self.points.index(point_line2)
        if (len(region) > 0) :
            regA = [] # list dari point yang berada di daerah kiri/atas
            regB = [] # list dari point yang berada di daerah kanan/bawah

            # Divide region
            for point in region :
                det = self.determinant(point_line1, point_line2, point)
                if (abs(det) < 1e-12) :
                    # dianggap ada di garis
                    self.contained.add(self.points.index(point))
                elif (det > 0) :
                    regA.append(point)
                elif (det < 0) :
                    regB.append(point)
                    

            a_is_not_contained = (len(regA) > 0 and not self.points.index(regA[0]) in self.contained)
            b_is_not_contained = (len(regB) > 0 and not self.points.index(regB[0]) in self.contained)

            new_triangleA_created = False
            new_triangleB_created = False


            # if any of the region is contained already, just skip
            # find furthest point in the not-contained area
            # then, update the vertices and lines
            if (a_is_not_contained) :
                furthestA = self.find_furthest_idx(point_line1, point_line2, regA)
                '''
                print("regA : ", regA)
                print("furthestA : ", furthestA) '''
                self.vertices.append(furthestA)
                self.lines.append([pl1_idx, furthestA])
                self.lines.append([pl2_idx, furthestA])
                # setelah terbentuk segitiga dalam region, update dulu point-point mana aja yang masuk ke segitiga
                self.update_contained(point_line1, point_line2, self.points[furthestA], regA)

                for point in regA :
                    if (self.points.index(point) in self.contained) :
                        regA.pop(regA.index(point))
                new_triangleA_created = (furthestA != -1)
                # bagi region menjadi yang lebih dekat dengan masing-masing
                self.findConvexHull(point_line1, self.points[furthestA], regA)
                self.findConvexHull(point_line2, self.points[furthestA], regA)
            if (b_is_not_contained) :
                furthestB = self.find_furthest_idx(point_line1, point_line2, regB)
                '''
                print("regB : ", regB)
                print("furthestB : ", furthestB) '''
                self.vertices.append(furthestB)
                self.lines.append([pl1_idx, furthestB])
                self.lines.append([pl2_idx, furthestB])
                self.update_contained(point_line1, point_line2, self.points[furthestB], regB)
                
                for point in regB :
                    if (self.points.index(point) in self.contained) :
                        regB.pop(regB.index(point))
                new_triangleB_created = (furthestB != -1)
                self.findConvexHull(point_line1, self.points[furthestB], regB)
                self.findConvexHull(point_line2, self.points[furthestB], regB)

            
            # delete the line created by point_line1 and point_line2
            if(new_triangleA_created or new_triangleB_created) :
                self.lines.pop(self.lines.index([pl1_idx, pl2_idx]))

    def visualize (self) :
        # berhubung kita cuma punya points sama lines yang berbentuk array
        plt.figure(figsize = (10, 6))
        colors = ['b','r','g']
        plt.title('Petal Width vs Petal Length')
        plt.xlabel('sepal length')
        plt.ylabel('sepal width')
        # sudah bikin 'ruang' untuk plot, waktunya memplot
        for point in self.points :
            plt.plot(point[0], point[1], 'bo')
        for line in self.lines :
            plt.plot([self.points[line[0]][0], self.points[line[1]][0]], [self.points[line[0]][1], self.points[line[1]][1]], 'bo-')
        plt.legend()
        plt.show()