# -*- coding:utf-8 -*-

from point import Point


class Triangle(object):
    """ Class representing a Triangle that is composed by
    three Point objects
    """

    def __init__(self, u, v, w):

        if not all(isinstance(point, Point) for point in (u, v, w)):
            raise TypeError("u, v, w must be Point objects", (u, v, w))

        self.u, self.v, self.w = u, v, w

    def __repr__(self):
        return "Triangle Object - ((%s, %s), (%s, %s), (%s, %s))" \
               % (self.u.x, self.u.y, self.v.x, self.v.y, self.w.x, self.w.y)

    def __iter__(self):
        yield self.u
        yield self.v
        yield self.w


# Testing class
if __name__ == "__main__":

    u = Point(0, 2)
    v = Point(2, 0)
    w = Point(5, 5)

    triangle = Triangle(u, v, w)
    print triangle
    print "Point u = %s" % str(triangle.u)
    print "Point v = %s" % str(triangle.v)
    print "Point w = %s" % str(triangle.w)

    # Testing class iterability
    for point in triangle:
        print point

    # Testing the exception
    Triangle(None, None, None)
