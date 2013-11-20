# -*- coding:utf-8 -*-

from point import Point


class Triangulation(object):
    """ Class that triangulates polygons with no hole """

    # Used to verify if triangulation is counter clockwise
    EPSILON = 0.0000000001

    def __init__(self, points):

        if not isinstance(points, list):
            raise TypeError("points must be a list")
        elif not all(isinstance(point, Point) for point in points):
            raise TypeError("elements of list must be Point objects")


    # TODO: If the points come sorted then it is not necessary to calculate
    # the Area 
    def area(self, points):
        """ Calculates the polygon area """
        
        area = 0
        n = len(points)
        p, q = n-1, 0
        
        while q < n:
            area += points[p].x*points[q].y - points[q].x*points[p].y
            q += 1
            p=q

        return area*0.5

    def process(self, points):
        """ Process and triangulates the polygon """

        # Minimum number of points to compose a triangle 
        if len(points) < 3:
            return False

        # Counter Clockwise polygon TODO: Verify if is necessary. See def area
        


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
        
        oppos = (triangle.v.x - triangle.u.x) * (triangle.w.y - triangle.u.y)
        adjac = (triangle.v.y - triangle.u.y) * (triangle.w.x - triangle.u.x)

        if EPSILON > (oppos - adjac):
            return False


# Testing the class
if __name__ == "__main__":

   pass 
