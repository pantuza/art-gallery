# -*- coding: utf-8 -*-

from point import Point
from triangulation import Triangulation
from coloring import Coloring
import threading
#import time

class ArtGallery(object):
    """ This class resolves The art gallery problem. 
    It is a visibility problem in computational geometry.
    Guarding an art gallery with the minimum number of guards who together
    can observe the whole gallery
    """

    def __init__(self, point):
        
        self._point = Point(point.id, point.x, point.y)
        self._points = [point]
        self._polygon = [(point.x, point.y)]
        self._triangulation = Triangulation(self._points)
        self._color = Coloring(self._points, self._triangulation)
        # for mult-tread preview
        self.lock = threading.RLock()
        self.version = 0
        
    @staticmethod
    def load(file_name):
        points = []
        with open(file_name, "r") as hfile:
            hfile.readline()
            i = 0
            for line in hfile:
                x, y = line.split()
                point = Point(i, int(x), int(y))
                i += 1
                points.append(point)
        return points

    def _update(self):
        self._points.sort()
        self._polygon = []
        for p in self._points:
            self._polygon.append((p.x, p.y))

    def get_polygon(self):
        with self.lock:
            return self._polygon

    def get_process_point(self):
        with self.lock:
            return self._point

    def get_points(self):
        with self.lock:
            return self._points

    def get_diagonals(self):
        with self.lock:
            return self._triangulation.get_diagonals()

    def get_min_color(self):
        with self.lock:
            return self._color.get_min_color()

    def is_guard(self, point):
        with self.lock:
            return point.color == self._color.get_min_color()

    def include(self, point):
        """ Add a new point to the art gallery """
        with self.lock:
            self._points.append(Point(point.id, point.x, point.y))
            self._update()
            # triangulate 
            #start = time.clock()
            triangulated = self._triangulation.process()
            #tt = time.clock() - start
            #print "Triangulating Time = "+ str(tt)
            if (triangulated):
                # coloring
                #start = time.clock()
                self._color.process()
                #ct = time.clock() - start
                #print "Coloring Time = "+ str(ct)
                #print "TT/CT = "+ str(tt/ct)
            # version control due to refresh of the painter object
            self.version += 1

if __name__ == '__main__':
        
        print "Starting..."
        tmp = ArtGallery.load("inputs/test_1.poly")
        g = ArtGallery(tmp.pop(0))
        for p in tmp:
            g.include(p)
        
        for p in g.get_points():
            if g.is_guard(p):
                print p, " GUARD!"
            else:
                print p
                
        print "Min_color = " + str(g._color.get_min_color())
        print "color[0] = " + str(g._color.get_color_count(0))
        print "color[1] = " + str(g._color.get_color_count(1))
        print "color[2] = " + str(g._color.get_color_count(2))
        print "color[3] = " + str(g._color.get_color_count(3))
        
            
        from preview_control import PreviewControl
        from art_gallery_painter import ArtGalleryPainter
        previewer = PreviewControl(ArtGalleryPainter)
        previewer.show(g, "Test")
            
        print "END!"

