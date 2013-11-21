# -*- coding: utf-8 -*-

from triangulation import Triangulation
from coloring import Coloring


class ArtGallery(object):
    """ This class resolves The art gallery problem. 
    It is a visibility problem in computational geometry.
    Guarding an art gallery with the minimum number of guards who together
    can observe the whole gallery
    """
    
    def __init__(self, points):
        
        self.points = points
        self.triangulation = Triangulation(self.points)
        self.coloring = Coloring()
        self.guards = []

    def include(self, data):
        """ Add a new point to the art gallery """

        self.points.append(data)
        self.points.sort()
        # triangulates 
        self.triangulation.process()
        # coloring 
        self.coloring.process()
