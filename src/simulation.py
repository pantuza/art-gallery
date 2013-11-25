# -*- coding: utf-8 -*-

from sys import argv
from sys import exit
import logging.config

from pymote.networkgenerator import NetworkGenerator
from pymote.simulation import Simulation
from pymote.conf import global_settings

from dist_art_gallery import DistributedArtGallery
from point import Point
from preview import Preview
from preview import PreviewDefaults
from preview_control import PreviewControl
from art_gallery_painter import ArtGalleryPainter
from art_gallery import ArtGallery

# Do not show log
logging.config.dictConfig({'version': 1, 'loggers': {}})

# VoronoiDiagram.start()
global_settings.ENVIRONMENT2D_SHAPE = (500, 500)


# Read the file name from command line
try:
    file_name = argv[1]
except IndexError:
    print "No input file"
    exit()

polygon = ArtGallery.load(file_name)
n_nodes = len(polygon)

# generates the network with 10 hosts
net_gen = NetworkGenerator(n_count=n_nodes-1, n_min=1, n_max=n_nodes)
net = net_gen.generate_random_network()

ArtGalleryPainter.set_polygon(polygon)

label = "Distributed Solution for Art Gallery Problem"

max_x = 0
max_y = 0
for p in polygon:
    
    # Correction on polygon draw on window
    if n_nodes < 7:
        p.x = ((p.x + 0) * 20) + 0
        p.y = ((p.y + 0) * 20) + 10

    if (p.x > max_x):
        max_x = p.x
    if (p.y > max_y):
        max_y = p.y

lines = PreviewDefaults.height // (max_y + 20)
columns = PreviewDefaults.width // (max_x + 20)

fps = 0

# Starts the graphical interface
PreviewControl.start(title=label,
                     lines=lines,
                     columns=columns,
                     fps_limit=fps,
                     painter_class=ArtGalleryPainter)


# Defines the network algorithm
net.algorithms = ((DistributedArtGallery, {'key': 'axis'}),)


i = 0
# Assign to node memory its position
for node in net.nodes():

    node.memory['axis'] = polygon[i]
    i += 1


# Creates and starts the simulation
sim = Simulation(net)
sim.run()

# Keep the main execution
while PreviewControl.in_state(Preview.RUNNING):
    pass

sim.reset()
