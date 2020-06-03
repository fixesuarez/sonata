'''
from utilities import colorWipe, wheel


class SoundLevelListener:
    
    def __init__(self, gpio_pin, nb_leds, freq_start, freq_end, soundgate):
        self.neopixel = Adafruit_NeoPixel(nb_leds, gpio_pin, LED_FREQ_HZ, 10, False, 255, 0)
        self.neopixel.begin()
        colorWipe(self.neopixel, Color(255, 0, 0))        
        self.index=0
        self.last_update=0 # last update in ms
        self.offset=40
        self.lvl_coeff=255./(soundgate)
        self.a=freq_start
        self.b=freq_end
        self.wide=freq_end-freq_start
        self.lastUpdate=millis()
        self.brightness=0
        self.color=wheel(255)
        self.last_level=0
        self.nb_leds=nb_leds
        print("Sound level listener initiated")
            
    def update(self, level, freq):
        print("sll updated : ", level, freq)
        m=millis()
        (dt, self.last_update)=(m-self.last_update, m)
        print "dt: "+str(dt)+"ms"
        
        
        if freq != None:
            if freq < self.b and freq>self.a:
                tmp_color=wheel(int((freq-self.a)/self.wide*(255-self.offset)+self.offset))
                
            diff_color=tmp_color-self.color
            self.color+=int(diff_color/dt)
            
        diff_level=self.last_level-level    
        self.last_level=level
        print("dl", diff_level, self.lvl_coeff)    
        self.brightness+=int((diff_level/dt*100)*self.lvl_coeff)
        
        if self.brightness<0:
            self.brightness=0
            
        if self.brightness>255:
            self.brightness=255
            
        if self.color>255:
            self.color=255
            
        if self.color<20:
            self.color=20
        
        for i in range(0, self.nb_leds):
            self.neopixel.setPixelColor(i, self.color)
             
        
        print("set ", self.brightness, self.color)
        self.neopixel.setBrightness(self.brightness)
        self.neopixel.show() 
        
    def fade(self):
        if(self.lastUpdate+90<millis()):
            if self.brightness>4:
                self.brightness-=5
        elif self.brightness<251:
            self.brightness+=5
            
        neopixel.setBrightness(self.brightness)
        neopixel.show()'''
