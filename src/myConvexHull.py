# myConvexHull.py

import math

class myConvexHull:

    def __init__(self, data) :
        self.points = data.tolist() # berisi point (point didefinisikan sebagai array of float dengan panjang 2 elemen)
        self.vertices = [] # berisi indeks dari point dalam points yang membentuk convex hull
        self.lines = [] # berisi point-point yang membentuk garis convex hull (didefinisikan sebagai array of integer dengan panjang 2 element)
        self.contained = set() # set yang berisi indeks dari point-point yang sudah berada di dalam area

        outer = self.find_outer_points()

        # since outer points surely create the convex hull
        self.vertices.append(self.points.index(outer[0]))
        self.vertices.append(self.points.index(outer[1]))
        self.lines.append([outer[0], outer[1]])
        self.contained.add(self.points.index(outer[0]))
        self.contained.add(self.points.index(outer[1]))

        init_reg = self.points.copy()
        left_point = outer[0]
        right_point = outer[1]
        init_reg.pop(init_reg.index(left_point))
        init_reg.pop(init_reg.index(right_point))

        self.findConvexHull(left_point, right_point, init_reg)


    def find_outer_points (self) :
        # mencari point-point dengan nilai absis terendah dan tertinggi
        # mengembalikan array dua elemen dalam bentuk [indeks point terkiri, indeks point terkanan]
        res = [self.points[0],self.points[0]]
        min_x = self.points[0][0]
        max_x = self.points[0][0]

        for point in self.points :
            if point[0] < min_x :
                min_x = point[0]
                res[0] = point
            if point[0] > max_x :
                max_x = point[0]
                res[1] = point
        return res

    def determinant(self, point_line1, point_line2, point) :
        # mencari nilai determinan untuk menentukan di daerah mana sebuah point berada
        # point_line1, point_line2, point : point
        # point_line1 dan point_line2 adalah ujung-ujung dari garis pembatas daerah
        det = (point_line1[0] * point_line2[1]) + (point[0] * point_line1[1]) + (point_line2[0] * point[1]) - (point[0] * point_line2[1]) - (point_line2[0] * point_line1[1]) - (point_line1[0] * point[1])
        return det

    def get_distance (self, p1, p2, point) :
        # menghitung jarak point dari garis yang dibentuk p1 dan p2
        a = p1[1] - p2[1]
        b = p2[0] - p1[0]
        c = (p1[0] * p2[1]) - (p2[0] * p1[1])
        denom = math.sqrt(a**2 + b**2)
        if (denom != 0) :
            return (abs(((a * point[0]) + (b * point[1]) + c)/denom))
        else :
            return -1

    def find_furthest_idx(self, point_line1, point_line2, region) :
        # mengembalikan indeks dari titik terjauh dengan garis dan memasukkan indeks yang bukan merupakan paling jauh ke dalam contained
        # dipastikan len(region) > 1
        furthest = -1
        idx = -1

        for point in region :
            dist = self.get_distance(point_line1, point_line2, point) 
            if (dist != -1 and dist > furthest) :
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

    def divide_region(self, p1, p2, p3, region) :
        # cari garis yang tegak lurus dengan garis yang dibentuk oleh titik p1 dan p2 dan melewati titik p3
        # bagi region berdasarkan tempat titik berada relatif terhadap garis tersebut
        reg1 = [] # berisi titik-titik yang berada di daerah yang sama dengan p1
        reg2 = [] # berisi titik-titik yang berada di daerah yang sama dengan p2
        
        # cari titik-titik yang memiliki nilai x lebih kecil dan lebih besar
        # x1 dan x2 tidak mungkin sama
        if p1[0] < p2[0] :
            left = p1
            right = p2
        else :
            left = p2
            right = p1

        # cari persamaan garis
        grad12 = (right[1] - left[1])/(right[0] - left[0])
        c12 = ((grad12 * left[0]) * -1) - left[1]
        if (grad12 != 0) :
            grad = -1/grad12
            c = ((grad * p3[0]) * -1) - p3[1]
            x = (c12 - c)/(grad - grad12)
            y = grad*x + c
        else : # p1 dan p2 memiliki nilai y yang sama
            x = p3[0]
            y = p1[1]
        
        # sign1 dan sign2 menandakan tanda dari determinan, True untuk + dan False untuk -
        sign1 = (self.determinant(p3, [x,y], p1) > 0)

        for point in region :
            sign = (self.determinant(p3, [x,y], point) > 0)
            if (sign==sign1) :
                reg1.append(point)
            else :
                reg2.append(point)

        return (reg1, reg2)

    def update_region (self, reg) :
        # menghapus elemen-elemen pada region yang sudah berada di dalam hull
        new_reg = []
        for point in reg :
            # abaikan point yang sudah berada di dalam bidang
            if not (self.points.index(point) in self.contained) :
                new_reg.append(point)

        reg = new_reg

    def findConvexHull (self, point_line1, point_line2, region) :
        # membentuk convex hull
        # region : array of points
        # point_line1, point_line2 : point
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
                else :
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

                self.vertices.append(furthestA)
                self.lines.append([point_line1, self.points[furthestA]])
                self.lines.append([point_line2, self.points[furthestA]])
                # setelah terbentuk segitiga dalam region, update dulu point-point mana aja yang masuk ke segitiga
                self.update_contained(point_line1, point_line2, self.points[furthestA], regA)
                self.update_region(regA)
                new_triangleA_created = (furthestA != -1)
                # bagi region menjadi yang lebih dekat dengan masing-masing
                regs = self.divide_region(point_line1, point_line2, self.points[furthestA], regA)
                self.findConvexHull(point_line1, self.points[furthestA], regs[0])
                self.findConvexHull(point_line2, self.points[furthestA], regs[1])

            if (b_is_not_contained) :
                furthestB = self.find_furthest_idx(point_line1, point_line2, regB)
    
                self.vertices.append(furthestB)
                self.lines.append([point_line1, self.points[furthestB]])
                self.lines.append([point_line2, self.points[furthestB]])
                self.update_contained(point_line1, point_line2, self.points[furthestB], regB)
                self.update_region(regB)
                new_triangleB_created = (furthestB != -1)

                regs = self.divide_region(point_line1, point_line2, self.points[furthestB], regB)
                self.findConvexHull(point_line1, self.points[furthestB], regs[0])
                self.findConvexHull(point_line2, self.points[furthestB], regs[1])

            
            # delete the line created by point_line1 and point_line2
            if(new_triangleA_created or new_triangleB_created) :
                self.lines.pop(self.lines.index([point_line1, point_line2]))