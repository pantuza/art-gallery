# -*- coding:utf-8 -*-

from point import Point
from triangle import Triangle


class Triangulation(object):
    """ Class that triangulates polygons with no hole """

    # Used to verify if triangulation is counter clockwise
    EPSILON = 0.0000000001

    def __init__(self, points):

        if not isinstance(points, list):
            raise TypeError("points must be a list")
        elif not all(isinstance(point, Point) for point in points):
            raise TypeError("elements of list must be Point objects")

        self.points = points

    # TODO: If the points come sorted then it is not necessary to calculate
    # the Area
    def area(self):
        """ Calculates the polygon area """

        area = 0
        n = len(self.points)
        p, q = n-1, 0

        while q < n:
            area += self.points[p].x * self.points[q].y \
                    - self.points[q].x * self.points[p].y
            q += 1
            p = q

        return area*0.5

    def process(self):
        """ Process and triangulates the polygon """
        import ipdb
        ipdb.set_trace()
        result = []

        # Minimum number of points to compose a triangle
        if len(self.points) < Triangle.MAX_POINTS:
            return False

        n_points = len(self.points)
        tmp_points = self.points[:]
        i = n_points - 1

        loop_control = 2 * n_points

        while len(tmp_points) > Triangle.MAX_POINTS:

            if loop_control <= 0:
                return Exception("Bla")
                

            # Creates a Triangle object with three consecutives Point objects
            triangle = Triangle(tmp_points[i % n_points],
                                tmp_points[(i+1) % n_points],
                                tmp_points[(i+2) % n_points])

            if self.snip(tmp_points, triangle):
                result.append(triangle)
                tmp_points.remove(tmp_points[i+1])

        del tmp_points
        return result

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
        c_cross = cx-apy - cy*apx

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
        return False


# Testing the class
if __name__ == "__main__":

    points = [Point(0, 0, 6),
              Point(1, 0, 0),
              Point(2, 3, 0),
              Point(3, 4, 1),
              Point(4, 6, 1),
              Point(5, 8, 0),
              Point(6, 12, 0),
              Point(7, 13, 2),
              Point(8, 8, 2),
              Point(9, 8, 4),
              Point(10, 11, 4),
              Point(11, 11, 6),
              Point(12, 6, 6),
              Point(13, 4, 3),
              Point(14, 2, 6)]

    triangulation = Triangulation(points)

    for triangle in triangulation.process():
        print "Triangle %d => (%s, %s) (%s, %s) (%s, %s)" \
              % (triangle.u.x, triangle.u.y,
                 triangle.v.x, triangle.v.y,
                 triangle.w.x, triangle.w.y)
