import sys
import math
import time
import traceback

from scipy.signal import fftconvolve
from socket import *
from pygame.locals import *
from random import *
import numpy

from neopixel import *
from rpi_ws281x import Adafruit_NeoPixel

from utilities import colorWipe
from constants import LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL


print("Setting up neopixels ...")
    
neopixel = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
neopixel.begin()
        
if __name__ == '__main__':
    loader = Loading(neopixel)
    loader.start()
    time.sleep(5) # un si beau loader faut quand meme lui laisser le temps de charger !
    
    try:
        note_listener = NoteListener(neopixel, 80, 710) # from 70 to 700Hz
        fade_worker = FadeWorker(note_listener, 50)
        fade_worker.start()
        
        #sll = SoundLevelListener(12, 7, 70, 700, 18) 
        
        note_trainer = NoteTrainer()
        note_trainer.addNoteListener(note_listener)
        #note_trainer.addSoundLevelListener(sll)
        note_trainer.main(loader)
        
    except KeyboardInterrupt:
        colorWipe(neopixel, Color(0,0,0), 50)
        fade_worker.stop()
