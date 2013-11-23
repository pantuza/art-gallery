# -*- coding: utf-8 -*-

class Coloring(object):

    def __init__(self, points, triangulation):
        self._points = points
        self._triangulation = triangulation
        self.colors = None
        self.min_color = 0
        self.sum_colors = [0, 0, 0, 0]

    def get_min_color(self):
        return self.min_color
    
    def get_color_count(self, color):
        return self.sum_colors[color]

    def _get_free_color(self, side):
        test = side.p0.color + side.p1.color
        if test == 3:
            return 3
        elif test == 4:
            return 2
        elif test == 5:
            return 1
        # Fail condition!
        return 0
    
    #def is_complete(self, triangle):
    #    return triangle.u.color + triangle.v.color + triangle.w.color == 6
    
    def _recursive_coloring(self, triangle, diagonal):
        # this triangle was visited?
        if (triangle in self._processed):
            return
        # if not, visit it...
        self._processed[triangle] = True

        # coloring the oposite side of diagonal
        point = triangle.opposite(diagonal)
        point.color = self._get_free_color(diagonal)

        # visit its neighbors (triangles with common side)
        for side in triangle.sides():
            # try all sides that differ from current processed diagonal
            if side != diagonal:
                # if side is a diagonal, then it has a opposite triangle
                neighbor = self._triangulation.get_opposite(triangle, side)
                if neighbor:
                    self._recursive_coloring(neighbor, side)

    def process(self):
        # clear the points colors
        for p in self._points:
            p.color = 0
        # do colorization
        # get the initial triangle 
        # (it must to have only one neighbor, but all sides will be tested) 
        triangle = self._triangulation.get_start()
        triangle.u.color = 2
        triangle.v.color = 1
        triangle.w.color = 3
        self._processed = {}
        self._processed[triangle] = True
        
        # visit its neighbors (triangles with common side)
        for side in triangle.sides():
            # if side is a diagonal, then it has a opposite triangle
            neighbor = self._triangulation.get_opposite(triangle, side)
            if neighbor:
                self._recursive_coloring(neighbor, side)

        # find the minimum color of the colorization
        self.min_color = self._min_color(self._points)
        
    def _min_color(self, points):
        # if any point has no color at this moment (color = 0), 
        # then the colorization has been wrong... 
        # but this failure won't be checked 
        # (here would be the best place to do this)  
        self.sum_colors = [0, 0, 0, 0]
        for point in points:
            self.sum_colors[point.color] += 1
        # compare color counts
        if self.sum_colors[1] <= self.sum_colors[2]:
            if self.sum_colors[1] <= self.sum_colors[3]:
                return 1
            else:
                return 3
        elif self.sum_colors[2] <= self.sum_colors[3]:
            return 2
        else:
            return 3

