from utilities import wheel, millis

class NoteListener:

    def __init__(self, neopixel, freq_start, freq_end):
        self.neopixel = neopixel
        self.index = 0
        self.offset = 0
        
        self.frequence_start = freq_start
        self.frequence_end = freq_end
        self.wide = freq_end-freq_start
        self.lastUpdate = millis()
        
        self.brightness=255
    
    
    def increment(self):
        self.index+=1
        if(self.index>=LED_COUNT):
            self.index=0
        self.lastUpdate=millis()
            
    def note(self, freq):
        print(freq, self.frequence_start, self.frequence_end)
        if freq < self.frequence_end and freq>self.frequence_start:
            ri=int((freq-self.frequence_start)/self.wide*(255-self.offset)+self.offset)
            #print(ri)
            self.neopixel.setPixelColor(self.index, wheel(ri) )
            self.neopixel.show()
            self.increment()
            
    def fade(self):
        if(self.lastUpdate+90<millis()):
            if self.brightness>4:
                self.brightness-=5
        elif self.brightness<251:
            self.brightness+=5
            
        self.neopixel.setBrightness(self.brightness)
        self.neopixel.show()
