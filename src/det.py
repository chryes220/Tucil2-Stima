def determinant(point_line1, point_line2, point) :
        # mencari nilai determinan untuk menentukan di daerah mana sebuah point berada
        # point_line1, point_line2, point : point
        # point_line1 dan point_line2 adalah ujung-ujung dari garis pembatas daerah
        det = (point_line1[0] * point_line2[1]) + (point[0] * point_line1[1]) + (point_line2[0] * point[1]) - (point[0] * point_line2[1]) - (point_line2[0] * point_line1[1]) - (point_line1[0] * point[1])
        return det


def is_contained(p1, p2, p3, point) :
        # menggunakan barycentric coordinate
        # referensi : https://mathworld.wolfram.com/TriangleInterior.html#:~:text=The%20simplest%20way%20to%20determine,it%20lies%20outside%20the%20triangle.

        denom = (p2[1] - p3[1])*(p1[0] - p3[0]) + (p3[0] - p2[0])*(p1[1] - p3[1])
        if (denom != 0) :
            a = ((p2[1] - p3[1])*(point[0] - p3[0]) + (p3[0] - p2[0])*(point[1] - p3[1])) / denom
            b = ((p3[1] - p1[1])*(point[0] - p3[0]) + (p1[0] - p3[0])*(point[1] - p3[1])) / denom
            c = 1 - a - b
            print("a, b, c ", a, b, c)
            return ((0 <= a <= 1) and (0 <= b <= 1) and (0 <= c <= 1))
        else :
            return False

import math
def get_distance (p1, p2, point) :
        # menghitung jarak point dari garis yang dibentuk p1 dan p2
        a = p1[1] - p2[1]
        b = p2[0] - p1[0]
        c = (p1[0] * p2[1]) - (p2[0] * p1[1])
        denom = math.sqrt(a**2 + b**2)
        if (denom != 0) :
            print(abs(((a * point[0]) + (b * point[1]) + c)/denom))
        else :
            print("denom = 0")

print(determinant([5.8, 4.0], [5.2,4.1], [5.7, 4.4]))
print(determinant([5.8, 4.0], [5.2,4.1], [5.5, 4.2]))