# -*- coding: utf-8 -*-


class Vector(object):
    """ Class representing a Vector """

    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return "Vector Object (%s, %s)" % (self.x, self.y)


# Testing class
if __name__ == "__main__":

    vector = Vector(5, 7)

    print vector
    print "x = %s" % vector.x
    print "y = %s" % vector.y
