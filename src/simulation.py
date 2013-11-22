# -*- coding: utf-8 -*-

from sys import argv
from sys import exit
import logging.config

from pymote.networkgenerator import NetworkGenerator
from pymote.simulation import Simulation
from pymote.conf import global_settings

from dist_art_gallery import DistributedArtGallery
from window import Window
from point import Point


# Do not show log
logging.config.dictConfig({'version': 1,'loggers':{}})

#VoronoiDiagram.start()
global_settings.ENVIRONMENT2D_SHAPE = (500, 500)


# Read the file name from command line
try:
    file_name = argv[1]
except IndexError:
    print "No input file"
    exit()

polygon = []

# Opens input file and reads the polygon
with open(file_name, "r") as file:

    # Read the first line that contains the number of vertices
    n_nodes = int(file.readline())
    id = 0
    for line in file:

        x, y = line.split()
        point = Point(id, x, y)
        polygon.append(point)
        id += 1


# generates the network with 10 hosts
net_gen = NetworkGenerator(n_count=n_nodes-1, n_min=1, n_max=n_nodes)
net = net_gen.generate_random_network()


# Defines the network algorithm
net.algorithms = ((DistributedArtGallery, {'key':'axis'}),)


i=0
# Assign to node memory its position
for node in net.nodes():

    node.memory['axis'] = polygon[i]
    i += 1


# Creates and starts the simulation
sim = Simulation(net)
sim.run()

# Show the State of the Voronoi Algorith execution
#print net.algorithmState

window = Window()
window.set_title("Distributed Solution for Art Gallery Problem")

# Plot voronoi diagram for each node
for node in net.nodes():
    
    try:
        print node.memory['axis']
    except AttributeError:
        print "%s Insufficient number of nodes to compute art gallery" % node


#VoronoiDiagram.stop()
sim.reset()
