"""
Preview of a Delaunay Triangulation and Voronoi Diagram using pygame.
"""
from __future__ import division
import pygame
from preview import Color

class ArtGalleryPainter(object):
    '''
    Painter of Voronoi Diagram by Delaunay Triangulation
    Must to have this interface:

    def __init__(self, number, view):
        """
        Receive a identification number and a object (view) to paint
        """
    def changed(self):
        """
        Informs if the state changed and need to draw a new version
        """
    def draw(self, panel):
        """
        Draw object in this panel
        """
    
    '''

    always_paint = False
    draw_diagonals = True
    draw_frame_counter = True
    draw_fps = True
    draw_version = True
    # radius of Voronoi site (in pixels)
    corner_radius = 4
    
    def __init__(self, number, view, label=''):
        self.number = number
        self.gallery = view
        self.version = -1
        self.label = label
        self.color = [Color.BLACK, Color.RED, Color.GREEN, Color.BLUE]
        self.process_color = pygame.Color(192, 192, 192)
        self.diagonal_color = pygame.Color(150, 222, 255)
    
    def changed(self):
        if (self.gallery.version != self.version):
            self.version = self.gallery.version
            return True
        return ArtGalleryPainter.always_paint

    def draw(self, panel, index):
        '''
        Automatically draw the art gallery to its panel
        '''
        # clear panel (pixel buffer)
        panel.clear()
        pointlist, triangulation, colorization = self.gallery.get_visual_data()
        if len(pointlist) > 1:
            surface = panel.surface
            # draw gallery
            pygame.draw.polygon(surface, Color.BLACK, 
                                pointlist, 2)
            pp = self.gallery.get_process_point()
            d = self.corner_radius + 6
            # draw current process
            rect = (pp.x - d,pp.y - d, 2*d, 2*d)
            pygame.draw.rect(surface, self.process_color, rect, 2)
            guard_color = colorization.get_min_color()
            for p in self.gallery.get_points():
                color = colorization.get_color(p)
                pygame.draw.circle(surface, self.color[color], 
                                   (p.x, p.y), self.corner_radius)
                if color == guard_color:
                    pygame.draw.circle(surface, self.color[color], 
                                       (p.x, p.y), self.corner_radius + 3, 2)

            if ArtGalleryPainter.draw_diagonals:
                color = pygame.Color(150, 222, 255)
                for line in triangulation.get_diagonals():
                    pygame.draw.line(surface, self.diagonal_color, 
                                     line[0], line[1])

        # draw labels
        label = str(index) + "/" + str(self.number) 
        label += " node:" + str(self.label)
        if ArtGalleryPainter.draw_fps:
            label += " - FPS:" + str(panel.fps)
        if ArtGalleryPainter.draw_frame_counter:
            label += "#" + str(panel.frame_counter)
        if ArtGalleryPainter.draw_version:
            label += "@" + str(self.version)
        panel.draw_line(label, Color.ORANGE)


