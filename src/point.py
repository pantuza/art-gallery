# -*- coding: utf-8 -*-


class Point(tuple):
    """ Represents a 2D point. Inherits built-in tuple """

    def __new__(cls, id, x, y):
        return tuple.__new__(cls, (int(id), int(x), int(y)))

    def __init__(self, id, x, y):
        super(Point, self).__init__(id, x, y)
        self.id = id
        self.x = x
        self.y = y

    def __repr__(self):
        return "Point(tuple) Object - P%s=(%s, %s)" % (self.id, self.x, self.y)


# Testing class
if __name__ == "__main__":

    point = Point(0, 3, 8)

    print point
    print "id = %s" % point.id
    print "x = %s" % point.x
    print "y = %s" % point.y

    for i in point:
        print i
