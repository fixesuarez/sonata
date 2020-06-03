from threading import Thread

class FadeWorker(Thread):
    
    def __init__(self, listener, delay):
        Thread.__init__(self)
        self.delay = delay
        self.listener = listener

    def run(self):
        self.go = True
        while self.go:
            self.listener.fade()
            time.sleep(self.delay/1000.)

    def stop(self):
        self.go = False
