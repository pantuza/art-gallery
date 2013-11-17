# -*- coding: utf-8 -*-

from pymote.algorithm import NodeAlgorithm
from pymote.message import Message


# TODO: This class is for test purpose
class ArtGallery(object):

    def include(self, data):
        pass


class DistributedArtGallery(NodeAlgorithm):
    """ Implements the distributed solution of the Art Gallery problem """

    # Host states
    STATUS = {'INITIATOR': 'initiator',
              'IDLE': 'idle',
              'DONE': 'done'}

    required_params = ('key',)
    default_params = {'neighborsKey': 'Neighbors'}

    def initializer(self):
        """ Method fot host initialization """

        for node in self.network.nodes():

            node.memory['neighbors_data'] = {}
            node.points = [node.memory['axis']]
            node.gallery = ArtGallery()

            # Fills node neighbors and notify each one its axis
            node.memory[self.neighborsKey] = \
                node.compositeSensor.read()['Neighbors']
            node.status = 'IDLE'

            self.notify(node, node.id, node.memory['axis'])

    def step(self, node):
        """ The step method is called every time a host receives a message """

        try:
            msg = node.receive()

            if msg is not None and msg.source != node:
                self.procmsg(node, msg)

        except Exception as e:
            raise Exception("Erro during processing message from node %s"
                            % node)

    def procmsg(self, node, msg):
        """ Process incoming messages """

        # If the message data (host position) is unknown
        if msg.data not in node.points:

            node.memory['neighbors_data'][msg.source.id] = msg.data
            node.points.append(msg.data)
            print node.id, msg.data

            # adds new point and recalculates the positions of the guards
            node.gallery.include(msg.data)

            # notifies the node neighbors about the message received
            self.notify(node, msg.source, msg.data)

    def notify(self, node, source, data):
        """ Notify neighbors. Forwarding operation """

        # Starts communication through neighbors nodes
        for neighbor in node.memory[self.neighborsKey]:

            msg = Message(header=NodeAlgorithm.INI, source=source,
                          destination=neighbor, data=data)

            node.send(msg)
