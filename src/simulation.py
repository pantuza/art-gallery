# -*- coding: utf-8 -*-

from sys import argv
from sys import exit
import logging.config

from pymote.networkgenerator import NetworkGenerator
from pymote.simulation import Simulation
from pymote.conf import global_settings


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
    
    for line in file:

        x, y = line.split()
        polygon.append((int(x),int(y)))

print polygon


# generates the network with 10 hosts
net_gen = NetworkGenerator(n_count=n_nodes-1, n_min=1, n_max=n_nodes)
net = net_gen.generate_random_network()

from pymote.algorithm import Algorithm
class DistributedArtGallery(Algorithm):
    pass

# Defines the network algorithm
net.algorithms = ((DistributedArtGallery, {'informationKey':'axis'}),)


i=0
# Assign to node memory its position
for node in net.nodes():
    node.memory['axis'] = (int(polygon[i][0]), int(polygon[i][1]))
    i += 1


# Creates and starts the simulation
sim = Simulation(net)
sim.run()

# Show the State of the Voronoi Algorith execution
#print net.algorithmState


# Plot voronoi diagram for each node
for node in net.nodes():
    
    try:
        print node.memory['axis']
    except AttributeError:
        print "%s Insufficient number of nodes to compute art gallery" % node


#VoronoiDiagram.stop()
sim.reset()
