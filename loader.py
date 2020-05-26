from threading import Thread
from constants import LED_COUNT


class Loader(Thread):
    def __init__(self, npx):
        Thread.__init__(self)
        self.loading=True
        self.rainbow=15;
        self.i=0;
        
    def next(self):
        if(self.rainbow<254):
            self.rainbow+=1;
        else:
            self.rainbow=15;
        
        if(self.i<LED_COUNT):
            self.i+=1;
        else:
            self.i=0;
        
        
    def stop(self):
        self.loading=False;
            
    def run(self):
        npx.setBrightness(255);
        while self.loading:
            npx.setPixelColor(self.i, wheel(self.rainbow));
            npx.show();
            self.next();
            time.sleep(0.007);
        

        print("program ready")