## NoteTrainer - by Alan Smith ##

import sys
import random
import os
import pyaudio
from scipy import signal
from socket import *
from pygame.locals import *
from random import *
import traceback
import numpy
from numpy import argmax, sqrt, mean, diff, log, nonzero, ravel

import time
from neopixel import *
from rpi_ws281x import Adafruit_NeoPixel

from constants import *
from utils import colorWipe
from note_listener import NoteListener
from note_trainer import NoteTrainer
from fade_worker import FadeWorker
from loader import Loader

from threading import Thread


print("Setting up neopixels ...");
    
neopixel = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
neopixel.begin()

if __name__ == '__main__':
    loader = Loader(neopixel)
    loader.start()
    time.sleep(7) # un si beau loader faut quand meme lui laisser le temps de charger !
    
    try:
        note_listener = NoteListener(neopixel, 70, 695) # from 70 to 700Hz
        note_listener_monitor = FadeWorker(note_listener, 50)
        note_listener_monitor.start()
        
        note_trainer = NoteTrainer()
        note_trainer.addNoteListener(note_listener)
        note_trainer.main(loader)
        
    except KeyboardInterrupt:
        colorWipe(neopixel, Color(0,0,0), 50)
        note_listener_monitor.stop()
