import time
from threading import Thread
from utilities import wheel

class Loading(Thread):
    def __init__(self, neopixel):
        Thread.__init__(self)
        self.loading = True
        self.rainbow = 15
        self.i = 0
        self.neopixel = neopixel
        
    def next(self):
        if(self.rainbow<254):
            self.rainbow += 1
        else:
            self.rainbow = 15
        
        if(self.i<LED_COUNT):
            self.i += 1
        else:
            self.i = 0
        
        
    def stop(self):
        self.loading=False
            
    def run(self):
        self.neopixel.setBrightness(255)
        while self.loading:
            self.neopixel.setPixelColor(self.i, wheel(self.rainbow))
            self.neopixel.show()
            self.next()
            time.sleep(0.007)

        print("program ready")
