# -*- coding:utf-8 -*-

from point import Point
from triangle import Triangle


class Triangulation(object):
    """ Class that triangulates polygons with no hole """

    # Used to verify if triangulation is counter clockwise
    EPSILON = 0.0000000001

    def __init__(self, points):

        if not isinstance(points, list):
            raise TypeError("_polygon must be a list")
        elif not all(isinstance(point, Point) for point in points):
            raise TypeError("elements of list must be Point objects")

        self._polygon = points
        self._diagonals = []

    def _set_indexes(self, v, n_points):
        """ Set indexes for triangulation based on v parameter """

        u = v
        if u >= n_points:
            u = 0

        v = u + 1
        if v >= n_points:
            v = 0

        w = v + 1
        if w >= n_points:
            w = 0

        return u, v, w

    def process(self):
        """ Process and triangulates the polygon """

        self._diagonals = []
        n_points = len(self._polygon)  # Controls the number of _polygon
        # Minimum number of _polygon to compose a triangle
        if n_points < 3:
            return False

        tmp_points = self._polygon[:]  # temporary list of _polygon
        if self.area() < 0.0:
            tmp_points.reverse()

        # controls the current triangle _polygon inside the while statement
        v = n_points - 1
        #u = v
        attempts = (2 * n_points)
        result = []
        while n_points > 3:

            if not attempts:
                self._diagonals = []
                return False
            attempts -= 1
            
            #starter = u
            u, v, w = self._set_indexes(v, n_points)

            # Creates a Triangle object with three consecutives Point objects
            triangle = Triangle(tmp_points[u], tmp_points[v], tmp_points[w])

            if self.snip(tmp_points, triangle):
                self._diagonals.append((tmp_points[u].get_pos(), 
                                        tmp_points[w].get_pos()))
                result.append(triangle)  # Adding current triangle to result
                tmp_points.remove(tmp_points[v])  # Removing current triangle
                #u = starter
                n_points -= 1
                attempts = (2 * n_points)

        triangle = Triangle(tmp_points[2], tmp_points[1], tmp_points[0])
        result.append(triangle)  # Adding last triangle to result
        del tmp_points
        return result
    
    def get_diagonals(self):
        return self._diagonals

    def is_inside(self, point, triangle):
        """ Verify if a given point belongs to a triangle inner area """

        ax, ay = triangle.w.x - triangle.v.x, triangle.w.y - triangle.v.y
        bx, by = triangle.u.x - triangle.w.x, triangle.u.y - triangle.w.y
        cx, cy = triangle.v.x - triangle.u.x, triangle.v.y - triangle.u.y

        apx, apy = point.x - triangle.u.x, point.y - triangle.u.y
        bpx, bpy = point.x - triangle.v.x, point.y - triangle.v.y
        cpx, cpy = point.x - triangle.w.x, point.y - triangle.w.y

        a_cross = ax*bpy - ay*bpx
        b_cross = bx*cpy - by*cpx
        c_cross = cx*apy - cy*apx

        return a_cross >= 0 and b_cross >= 0 and c_cross >= 0

    def snip(self, points, triangle):
        """Return true if the polygon can be snipped """

        oppos = (triangle.v.x - triangle.u.x) * (triangle.w.y - triangle.u.y)
        adjac = (triangle.v.y - triangle.u.y) * (triangle.w.x - triangle.u.x)

        if self.EPSILON > (oppos - adjac):
            return False

        # verify if the point belongs to the triangle
        for point in points:
            if point not in triangle and self.is_inside(point, triangle):
                return False
        return True

    def area(self):
        size = len(self._polygon)
        area = 0.0
        i0 = size -1
        i1 = 0
        while i1 < size:
            area += self._polygon[i0].x * self._polygon[i1].y - \
                    self._polygon[i0].y * self._polygon[i1].x
            i0 = i1 
            i1 += 1
        return (area / 2)

# Testing the class
if __name__ == "__main__":

    points = [Point(0, 0, 6),
              Point(11, 11, 6),
              Point(2, 3, 0),
              Point(4, 6, 1),
              Point(1, 0, 0),
              Point(5, 8, 0),
              Point(13, 4, 3),
              Point(6, 12, 0),
              Point(7, 13, 2),
              Point(8, 8, 2),
              Point(9, 8, 4),
              Point(10, 11, 4),
              Point(3, 4, 1),
              Point(12, 6, 6),
              Point(14, 2, 6)]
    
    points.sort()
    triangulation = Triangulation(points)
    triangles = triangulation.process()
    from coloring import Coloring
    color = Coloring(points)
    if triangles:
        color.process(triangles)
        i = 1
        for t in triangles:
            print "Triangle %d => (%s,%s)[%s] (%s,%s)[%s] (%s,%s)[%s]" \
               % (i, t.u.x, t.u.y, color.get_color(t.u),
                     t.v.x, t.v.y, color.get_color(t.v),
                     t.w.x, t.w.y, color.get_color(t.w))
            if points.count(t.v) != 1:
                print "Where is v " + t.v
            if points.count(t.u) != 1:
                print "Where is u " + t.u
            if points.count(t.w) != 1:
                print "Where is w " + t.w
            i += 1
            
            
