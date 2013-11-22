"""
Preview of a Delaunay Triangulation and Voronoi Diagram using matplotlib.
"""
from __future__ import division
import random
import threading 
from preview import Preview, PreviewDefaults
from preview_control import PreviewControl 
from art_gallery import ArtGallery
from art_gallery_painter import ArtGalleryPainter

class TestProcess(threading.Thread):
    '''
    Generate a mono and mult thread test for Art Gallery Previewer
    '''
    STARTING = 1
    RUNNING = 2
    STOPPING = 3
    
    num_threads = 0
    lock = threading.Lock()
    _big_delay = 0.25
    
    def __init__(self, points, index_main_point, delay):
        with TestProcess.lock:
            self.id = TestProcess.num_threads
            TestProcess.num_threads += 1
            self._polygon = points[:]
            self.gallery = ArtGallery(self._polygon.pop(index_main_point))
        self.delay = delay
        self.big_delay = TestProcess._big_delay \
                         if delay < TestProcess._big_delay \
                         else delay
        self.state = TestProcess.STARTING
        threading.Thread.__init__(self)
        self.counter = 0
        

    def start(self):
        threading.Thread.start(self)

    def stop(self):
        self.state = TestProcess.STOPPING
        
    def must_exit(self):
        self.counter += 1
        threading.Event().wait(self.delay)
        return self.state != TestProcess.RUNNING

    def must_exit_delay(self, delay):
        self.counter += 1
        threading.Event().wait(delay)
        return self.state != TestProcess.RUNNING

    def run(self):
        self.state = TestProcess.RUNNING
        while True:
            size = len(self._polygon)
            if size == 0 or self.must_exit(): break
            index = random.randint(0, size - 1)
            point = self._polygon.pop(index)
            self.gallery.include(point)
        # keep running until receive a stop sign
        while self.state == TestProcess.RUNNING:
            pass

class TestCases(object):

    def simple(self):
        # simple test without cleanup:
        assert len(self._polygon) > 3 
        gallery = ArtGallery(self._polygon.pop(self.main_index))
        for point in self._polygon:
            gallery.include(point)
                
        self.preview_control.show(gallery, title = "Without cleanup")

    # linux only (due to pygame)
    def thread(self, points, preview):
        # configure
        threads = []
        # create tests in different threads
        size = len(points)
        for i in xrange(0,size):
            test = TestProcess(points, i, self.delay)
            threads.append(test)
            preview.add_view(test.gallery, str(i))
            test.start()

        return threads
            
    def do_test(self, file_name, s = 1, d = 1, mx = 0, my = 0):
        
        self.set_cenario(file_name)
        self.transform(s, s, d, d, mx, my)
        self.set_limits()
        
        label = "Multithread test : " + file_name
        import platform
        if platform.system() == "Linux":
            label += " (Linux)" 
            self.preview_control.start(title = label, 
                      lines = self.lines, columns = self.columns, 
                      fps_limit = self.fps, painter_class = ArtGalleryPainter)
            threads = self.thread(self._polygon, self.preview_control)
            # waiting until previewer terminates
            while self.preview_control.in_state(Preview.RUNNING):
                pass
        else:
            label += " (Windows)"
            preview = Preview(title = label, 
                      lines = self.lines, columns = self.columns, 
                      fps_limit = self.fps, painter_class = ArtGalleryPainter)
            preview.interactive(True)
            preview.start()
            threads = self.thread(self._polygon, preview)
            while preview.step():
                pass
        # stop tests threads
        for t in threads:
            t.stop()

    def transform(self, sx, sy, dx, dy, mx, my):
        for p in self._polygon:
            p.x = ((p.x + dx) * sx) + mx
            p.y = ((p.y + dy) * sy) + my

    def set_limits(self):
        max_x = 0
        max_y = 0
        for p in self._polygon:
            if (p.x > max_x): max_x = p.x
            if (p.y > max_y): max_y = p.y
        self.columns = PreviewDefaults.width // (max_x + 20)
        self.lines = PreviewDefaults.height // (max_y + 20)
 
    def __init__(self):
        pass

    def set_cenario(self, file_name):
        self.delay = 0.25
        self._polygon = ArtGallery.load(file_name)
        self.preview_control = PreviewControl(ArtGalleryPainter)
        self.fps = 0


if __name__ == '__main__':

    test = TestCases()
    test.do_test("../inputs/test_0.poly")
    test.do_test("../inputs/test_1.poly")
    test.do_test("../inputs/test_2.poly")
    test.do_test("../inputs/regular_0.poly", 20, 1, 0, 10)
    test.do_test("../inputs/regular_1.poly", 5, 1, 0, 20)
    test.do_test("../inputs/irregular_0.poly", 15, 1)
