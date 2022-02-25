# myConvexHull.py

import matplotlib.pyplot as plt
import math

class myConvexHull:
    points = [] # berisi point (point didefinisikan sebagai array of float dengan panjang 2 elemen)
    vertices = [] # berisi indeks dari point dalam points yang membentuk convex hull
    lines = [] # berisi indeks dari point-point yang membentuk garis convex hull (didefinisikan sebagai array of integer dengan panjang 2 element)
    outer = [] # berisi indeks dari dua point terluar, dengan points[outer[0]][0] < points[outer[1]][0]
    contained = [] # berisi indeks dari point-point yang sudah berada di dalam area

    def __init__(self, arr_of_points) :
        # points dalam parameter bertipe array
        self.points = arr_of_points

        self.outer = self.find_outer_points()
        # since outer points surely create the convex hull
        self.vertices.append(self.outer[0])
        self.vertices.append(self.outer[1])
        self.lines.append([self.outer[0], self.outer[1]])

        self.findConvexHull(self.points[self.outer[0]], self.points[self.outer[1]], self.points)

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
            elif self.points[i][0] > max_x :
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
            dist = abs(((a * point[0]) + (b * point[1]) + c)/math.sqrt(a**2 + b**2))
            if (dist > furthest) :
                furthest = dist
                idx = self.points.index(point)
        return idx

    def update_contained(self, p1, p2, p3, region) :
        # p3 adalah bagian dari region
        # referensi : https://mathworld.wolfram.com/TriangleInterior.html#:~:text=The%20simplest%20way%20to%20determine,it%20lies%20outside%20the%20triangle.
        for point in region :
            div = (p2[1] - p3[1])*(p1[0] - p3[0]) + (p3[0] - p2[0])*(p1[1] - p3[1])
            if (div != 0) :
                a = ((p2[1] - p3[1])*(point[0] - p3[0]) + (p3[0] - p2[0])*(point[1] - p3[1])) / div
                b = ((p3[1] - p1[1])*(point[0] - p3[0]) + (p1[0] - p3[0])*(point[1] - p3[1])) / div
                c = 1 - a - b

                if (0 <= a <= 1 and 0 <= b <= 1 and 0 <= c <= 1) :
                    # titik ada di dalam segitiga
                    self.contained.append(self.points.index(point))

    def findConvexHull (self, point_line1, point_line2, region) :
        # region : array of points
        # point_line1, point_line2 : point

        pl1_idx = self.points.index(point_line1)
        pl2_idx = self.points.index(point_line2)
        if (len(region) > 0) :
            regA = [] # list dari point yang berada di daerah kiri/atas
            regB = [] # list dari point yang berada di daerah kanan/bawah

            # Divide region
            for point in region :
                det = self.determinant(point_line1, point_line2, point)
                if (det > 0) :
                    regA.append(point)
                elif (det < 0) :
                    regB.append(point)
                # semua point yang berada pada garis diabaikan

            #print("region A ", regA)
            #print("region B", regB)

            # if any of the region is contained already, just skip
            # find furthest point in the not-contained area
            # then, update the vertices and lines
            if (len(regA) > 0 and not (regA[0] in self.contained)) :
                furthestA = self.find_furthest_idx(point_line1, point_line2, regA)
                #print("furthestA : ", furthestA)
                self.vertices.append(furthestA)
                self.lines.append([pl1_idx, furthestA])
                self.lines.append([pl2_idx, furthestA])
                self.update_contained(point_line1, point_line2, self.points[furthestA], regA)
                # next iteration
                self.findConvexHull(point_line1, self.points[furthestA], regA)
                self.findConvexHull(point_line2, self.points[furthestA], regA)
            if (len(regB) > 0 and not (regB[0] in self.contained)) :
                furthestB = self.find_furthest_idx(point_line1, point_line2, regB)
                #print("furthestB : ", furthestB)
                self.vertices.append(furthestB)
                self.lines.append([pl1_idx, furthestB])
                self.lines.append([pl2_idx, furthestB])
                self.update_contained(point_line1, point_line2, self.points[furthestB], regB)
                # next iteration
                self.findConvexHull(point_line1, self.points[furthestB], regB)
                self.findConvexHull(point_line2, self.points[furthestB], regB)
            
            # delete the line created by point_line1 and point_line2
            self.lines.pop(self.lines.index([pl1_idx, pl2_idx]))

