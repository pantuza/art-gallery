# -*- coding: utf-8 -*-

from preview import Preview


class PreviewControl(object):
    """ 
    This class is a controler for preview. 
    """

    preview = None

    def __init__(self, painter_class = None):
        self.painter_class = painter_class

    @staticmethod
    def start(**args):
        '''
        Automatic create a default previewer object
        '''
        PreviewControl.preview = Preview(**args)
        PreviewControl.preview.start()

    @staticmethod
    def stop():
        '''
        Stop the default previewer
        '''
        PreviewControl.preview.stop()

    @staticmethod
    def add_view(element, label=''):
        '''
        Include a diagram into the default previewer
        '''
        #print "new_diagram call: label=%s" % label
        PreviewControl.preview.add_view(element, label)

    @staticmethod
    def in_state(state):
        '''
        Checks the state of the default preview
        '''
        if PreviewControl.preview is None: 
            return state == Preview.NONE
        return state == PreviewControl.preview.state

    @staticmethod
    def show(view, title = '', lines = 1, columns = 1):
        preview = Preview(title = title, lines = lines, columns = columns,
                          painter_class = self.painter_class)
        preview.add_view(view, title)
        preview.interactive(True)
        preview.start()
        while preview.step():
            pass
