
from utils import wheel, millis

class NoteListener:

    def __init__(self, npx, freq_start, freq_end):
        self.npx=npx
        self.index=0
        self.offset=40
        
        self.a=freq_start
        self.b=freq_end
        self.wide=freq_end-freq_start
        self.lastUpdate=millis()
        
        self.brightness=255
        
            
    def note(self, freq):
        print(freq, self.a, self.b)
        if freq < self.b and freq>self.a:
            ri=int((freq-self.a)/self.wide*(255-self.offset)+self.offset)
            print(ri)
            self.npx.setPixelColor(self.index, wheel(ri) )
            self.npx.show()
            self.increment()


    def increment(self):
        self.index+=1
        if(self.index>=LED_COUNT):
            self.index=0
        self.lastUpdate=millis()


    def fade(self):
        if(self.lastUpdate + 90 < millis()):
            if self.brightness>4:
                self.brightness-=5
        elif self.brightness<251:
            self.brightness+=5
            
        npx.setBrightness(self.brightness)
        npx.show()
