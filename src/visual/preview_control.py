# -*- coding: utf-8 -*-

from preview import Preview

class PreviewControl(object):
    """ This class is a controler for preview. 
    
    """

    def __init__(self, painter_class = None):
        self.preview = None
        self.painter_class = painter_class

    def start(self, **args):
        '''
        Automatic create a default previewer object
        '''
        self.preview = Preview(**args)
        self.preview.start()

    def stop(self):
        '''
        Stop the default previewer
        '''
        self.preview.stop()

    def add_view(self, element, label=''):
        '''
        Include a diagram into the default previewer
        '''
        #print "new_diagram call: label=%s" % label
        self.preview.add_view(element, label)

    def in_state(self, state):
        '''
        Checks the state of the default preview
        '''
        if self.preview is None: 
            return state == Preview.NONE
        return state == self.preview.state

    def show(self, view, title = '', lines = 1, columns = 1):
        preview = Preview(title = title, lines = lines, columns = columns,
                          painter_class = self.painter_class)
        preview.add_view(view, title)
        preview.interactive(True)
        preview.start()
        while preview.step():
            pass
        
