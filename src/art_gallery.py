# -*- coding: utf-8 -*-

from point import Point
from triangulation import Triangulation
from coloring import Coloring
import threading

class ArtGallery(object):
    """ This class resolves The art gallery problem. 
    It is a visibility problem in computational geometry.
    Guarding an art gallery with the minimum number of guards who together
    can observe the whole gallery
    """

    def __init__(self, point):
        
        self._point = point
        self._points = [point]
        self._polygon = [(point.x, point.y)]
        self._triangulation = Triangulation(self._points)
        self._color = Coloring(self._points)
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

    def get_process_point(self):
        return self._point
        
    def get_positions(self):
        with self.lock:
            return self._polygon

    def get_points(self):
        with self.lock:
            return self._points

    def is_guard(self, point):
        with self.lock:
            return self._color.get_color(point) == self._color.get_min_color()

    def include(self, point):
        """ Add a new point to the art gallery """
        with self.lock:
            self._points.append(point)
            self._update()
            # triangulates 
            triangles = self._triangulation.process()
            # coloring
            if (triangles):
                self._color.process(triangles)
            # version control due to refresh of the painter object
            self.version += 1

    def get_visual_data(self):
        with self.lock:
            return self._polygon, self._triangulation, self._color
        
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
        print "color[0] = " + str(g._color.color[0])
        print "color[1] = " + str(g._color.color[1])
        print "color[2] = " + str(g._color.color[2])
        print "color[3] = " + str(g._color.color[3])
        
            
        from preview_control import PreviewControl
        from art_gallery_painter import ArtGalleryPainter
        previewer = PreviewControl(ArtGalleryPainter)
        previewer.show(g, "Test")
            
        print "END!"

