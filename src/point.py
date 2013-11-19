# -*- coding: utf-8 -*-


class Point(tuple):
    """ Represents a 2D point. Inherits built-in tuple """

    def __new__(cls, x, y):
        return tuple.__new__(cls, (int(x), int(y)))

    def __init__(self, x, y):
        super(Point, self).__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return "Point(tuple) Object - (%s, %s)" % (self.x, self.y)


# Testing class
if __name__ == "__main__":

    point = Point(3, 8)

    print point
    print "x = %s" % point.x
    print "y = %s" % point.y

    for i in point:
        print i
