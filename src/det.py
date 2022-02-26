def determinant(point_line1, point_line2, point) :
        # mencari nilai determinan untuk menentukan di daerah mana sebuah point berada
        # point_line1, point_line2, point : point
        # point_line1 dan point_line2 adalah ujung-ujung dari garis pembatas daerah
        det = (point_line1[0] * point_line2[1]) + (point[0] * point_line1[1]) + (point_line2[0] * point[1]) - (point[0] * point_line2[1]) - (point_line2[0] * point_line1[1]) - (point_line1[0] * point[1])
        return det

print(determinant([4.6,3.1], [5.1,3.5], [5.1,3.5]))
print(1e-15)