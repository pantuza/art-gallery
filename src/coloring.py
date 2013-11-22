# -*- coding: utf-8 -*-


class Coloring(object):

    def __init__(self, points):
        self._polygon = points
        self.colors = None
        self.min_color = 0

    def get_color(self, point):
        if self.colors:
            return self.colors.get(point, 0)
        return 0
    
    def get_min_color(self):
        return self.min_color
    
    def process(self, triangles):
        self.colors = dict.fromkeys(self._polygon, 0)
        self.min_color
        # do colorization
        i = 0
        for t in triangles:
            free_color = [ True, True, True, True]
            color_u = self.colors[t.u]
            color_v = self.colors[t.v]
            color_w = self.colors[t.w]
            free_color[color_u] = False
            free_color[color_v] = False
            free_color[color_w] = False
            if (not color_u):
                color_u = 1 if free_color[1] else 2 if free_color[2] else 3
                free_color[color_u] = False
                self.colors[t.u] = color_u
            if (not color_v):
                color_v = 1 if free_color[1] else 2 if free_color[2] else 3
                free_color[color_v] = False
                self.colors[t.v] = color_v
            if (not color_w):
                color_w = 1 if free_color[1] else 2 if free_color[2] else 3
                self.colors[t.w] = color_w
            i += 1
            print "Triangle %d => (%s,%s)[%s] (%s,%s)[%s] (%s,%s)[%s]" \
               % (i, t.u.x, t.u.y, self.colors[t.u],
                     t.v.x, t.v.y, self.colors[t.v],
                     t.w.x, t.w.y, self.colors[t.w])
        # count the colors
        self.color = [ 0, 0, 0, 0]
        for p in self._polygon:
            self.color[self.colors[p]] += 1
        # check colorization
        if (self.color[0]):
            return False
        # find the minimum
        if self.color[1] <= self.color[2]:
            if self.color[1] <= self.color[3]:
                self.min_color = 1
            else:
                self.min_color = 3
        elif self.color[2] <= self.color[3]:
                self.min_color = 2
        else:
            self.min_color = 3
        return True

