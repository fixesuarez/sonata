## NoteTrainer - by Alan Smith ##

import sys
import random
import math
import os
import pyaudio
from scipy import signal
from socket import *
from pygame.locals import *
from random import *
import traceback
import numpy
from scipy.signal import blackmanharris, fftconvolve
from numpy import argmax, sqrt, mean, diff, log, nonzero, ravel

import time
from neopixel import *
from rpi_ws281x import Adafruit_NeoPixel

import argparse

from utils import wheel
from note_listener import NoteListener
from fade_worker import FadeWorker

from threading import Thread


# LED strip configuration:
LED_COUNT      = 15      # Number of LED pixels.
LED_PIN        = 18     # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


print("Setting up neopixels ...");
    
npx = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
npx.begin();

def find(condition):
    res, = nonzero(ravel(condition))
    return res


def colorWipe(strip, color, wait_ms=50, inverse=False):
    """Wipe color across display a pixel at a time."""
    tab=range(strip.numPixels(), -1, -1) if inverse else range(strip.numPixels())
    for i in tab:
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

# See http://www.swharden.com/blog/2013-05-09-realtime-fft-audio-visualization-with-python/
class SoundRecorder:

    def __init__(self):
        self.RATE=44100
        self.BUFFERSIZE=1024 #1024 is a good buffer size 3072 works for Pi
        self.secToRecord=.05
        self.threadsDieNow=False
        self.newAudio=False
        
       
        p=pyaudio.PyAudio()
        print("scanning input devices ...")

        self.device_index=0

        for i in range(p.get_device_count()):
            dev = p.get_device_info_by_index(i)
            print((i,dev['name'],dev['maxInputChannels']))
            if 'USB' in dev['name']:
                self.device_index=i

        print("Using device no ", self.device_index)

    def setup(self):
        self.buffersToRecord=int(self.RATE*self.secToRecord/self.BUFFERSIZE)
        if self.buffersToRecord==0: self.buffersToRecord=1
        self.samplesToRecord=int(self.BUFFERSIZE*self.buffersToRecord)
        self.chunksToRecord=int(self.samplesToRecord/self.BUFFERSIZE)
        self.secPerPoint=1.0/self.RATE
        self.p = pyaudio.PyAudio()
        self.inStream = self.p.open(input_device_index=self.device_index, format=pyaudio.paInt16,channels=1,rate=self.RATE,input=True,frames_per_buffer=self.BUFFERSIZE)
        self.xsBuffer=numpy.arange(self.BUFFERSIZE)*self.secPerPoint
        self.xs=numpy.arange(self.chunksToRecord*self.BUFFERSIZE)*self.secPerPoint
        self.audio=numpy.empty((self.chunksToRecord*self.BUFFERSIZE),dtype=numpy.int16)



    def close(self):
        self.p.close(self.inStream)

    def getAudio(self):
        audioString=self.inStream.read(self.BUFFERSIZE)
        self.newAudio=True
        return numpy.fromstring(audioString,dtype=numpy.int16)

# See https://github.com/endolith/waveform-analyzer/blob/master/frequency_estimator.py
def parabolic(f, x):
    xv = 1/2. * (f[x-1] - f[x+1]) / (f[x-1] - 2 * f[x] + f[x+1]) + x
    yv = f[x] - 1/4. * (f[x-1] - f[x+1]) * (xv - x)
    return (xv, yv)

# See https://github.com/endolith/waveform-analyzer/blob/master/frequency_estimator.py
def freq_from_autocorr(raw_data_signal, fs):
    corr = fftconvolve(raw_data_signal, raw_data_signal[::-1], mode='full')
    corr = corr[int(math.floor(len(corr)/2)):]
    d = diff(corr)
    start = find(d > 0)[0]
    peak = argmax(corr[start:]) + start
    px, py = parabolic(corr, peak)
    return fs / px

def loudness(chunk):
    data = numpy.array(chunk, dtype=float) / 32768.0
    ms = math.sqrt(numpy.sum(data ** 2.0) / len(data))
    if ms < 10e-8: ms = 10e-8
    return 10.0 * math.log(ms, 10.0)



def find_nearest(array, value):
    index = (numpy.abs(array - value)).argmin()
    return array[index]

def closest_value_index(array, guessValue):
    # Find closest element in the array, value wise
    closestValue = find_nearest(array, guessValue)
    # Find indices of closestValue
    indexArray = numpy.where(array==closestValue)
    # Numpys 'where' returns a 2D array with the element index as the value
    return indexArray[0][0]

def build_default_tuner_range():
    return {65.41:'C2',
            69.30:'C2#',
            73.42:'D2',
            77.78:'E2b',
            82.41:'E2',
            87.31:'F2',
            92.50:'F2#',
            98.00:'G2',
            103.80:'G2#',
            110.00:'A2',
            116.50:'B2b',
            123.50:'B2',
            130.80:'C3',
            138.60:'C3#',
            146.80:'D3',
            155.60:'E3b',
            164.80:'E3',
            174.60:'F3',
            185.00:'F3#',
            196.00:'G3',
            207.70:'G3#',
            220.00:'A3',
            233.10:'B3b',
            246.90:'B3',
            261.60:'C4',
            277.20:'C4#',
            293.70:'D4',
            311.10:'E4b',
            329.60:'E4',
            349.20:'F4',
            370.00:'F4#',
            392.00:'G4',
            415.30:'G4#',
            440.00:'A4',
            466.20:'B4b',
            493.90:'B4',
            523.30:'C5',
            554.40:'C5#',
            587.30:'D5',
            622.30:'E5b',
            659.30:'E5',
            698.50:'F5',
            740.00:'F5#',
            784.00:'G5',
            830.60:'G5#',
            880.00:'A5',
            932.30:'B5b',
            987.80:'B5',
            1047.00:'C6',
            1109.0:'C6#',
            1175.0:'D6',
            1245.0:'E6b',
            1319.0:'E6',
            1397.0:'F6',
            1480.0:'F6#',
            1568.0:'G6',
            1661.0:'G6#',
            1760.0:'A6',
            1865.0:'B6b',
            1976.0:'B6',
            2093.0:'C7'
            }

class NoteTrainer(object):
    def addNoteListener(self, noteListener):
        self.noteListener=noteListener;
        
    def __init__(self):
        self.noteListener=None    
        
        # Build frequency, noteName dictionary
        self.tunerNotes = build_default_tuner_range()
        # Sort the keys and turn into a numpy array for logical indexing
        self.frequencies = numpy.array(sorted(self.tunerNotes.keys()))
        
    def main(self, loader):
        print("initiating vars ...")
        stepsize = 5

        tunerNotes=self.tunerNotes;
        frequencies=self.frequencies;

        top_note = len(tunerNotes)-1
        bot_note = 0

        top_note = 24
        bot_note = 0

        # Misc variables for program controls
        inputnote = 1                               # the y value on the plot
        shownotes = True                            # note names shown or invisible
        signal_level=0                              # volume level
        fill = True                                 #
        trys = 1
        needle = False
        cls = True
        col = False
        circ = False
        line = False
        auto_scale = False
        toggle = False
        stepchange = False
        soundgate = 17.5                            # zero is loudest possible input level
        targetnote=0
        print("initiating sound recorder ...");
        SR=SoundRecorder()                          # recording device (usb mic)
        print("SR intiated", trys);
        loader.stop();
        while True:
            SR.setup()
            raw_data_signal = SR.getAudio()
            signal_level = round(abs(loudness(raw_data_signal)),2)                  #### find the volume from the audio sample
          
            try:
                fr=freq_from_autocorr(raw_data_signal,SR.RATE);
                inputnote = round(fr,2)
            except Exception as e:
                inputnote = 0
                
            SR.close()

            if inputnote > frequencies[len(tunerNotes)-1]:                        #### not interested in notes above the notes list
                continue

            if inputnote < frequencies[0]:                                     #### not interested in notes below the notes list
                continue

            if signal_level > soundgate:                                        #### basic noise gate to stop it guessing ambient noises
                continue

            #print("frequence: ", inputnote, "Hz");
            #print("tuner note ", tunerNotes[frequencies[targetnote]])
            #print("signal level", signal_level)

            targetnote = closest_value_index(frequencies, round(inputnote, 2))
            
            ##### use the controls to make changes to the data #####
            print("level, freq, tuner_note, target_note", signal_level, str(inputnote)+"Hz", tunerNotes[frequencies[targetnote]], targetnote);
            if self.noteListener!=None:
                self.noteListener.note(inputnote)
                
            if stepchange == True:                     #go to start of the loop if the step size is altered
                stepchange = not stepchange
                break

            if auto_scale:
                if bot_note < 55 and bot_note < top_note + 6:
                    bot_note = targetnote - 6
                if top_note > 5 and top_note > bot_note + 6:
                    top_note = targetnote  + 6
                auto_scale = False

            if col:
                err = abs(frequencies[targetnote]-inputnote)
                if err < 1.0:
                    stepsizecolor = (0,255,0)
                if err >= 1.0 and err <=2.5:
                    stepsizecolor = (255,255,255)
                if err > 2.5:
                    stepsizecolor = (255,0,0)

            if circ:
                print('circ: ', abs(int(20-signal_level)*3))

            if needle:
                print('needle', inputnote)



            #### memory of position

            ####### Draw Stuff on the screen #######


            # display note names if selected
            if shownotes:
                print("signal_level", signal_level)
                err = abs(frequencies[targetnote]-inputnote)
                print("note & err", tunerNotes[frequencies[targetnote]], err)

class Loading(Thread):
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
        

= '__main__':
    loader=Loading(npx);
    loader.start();
    time.sleep(7); # un si beau loader faut quand meme lui laisser le temps de charger !
    
    try:
        nl=NoteListener(npx, 70, 695); # from 70 to 700Hz
        nl_monitor=FadeWorker(nl, 50);
        nl_monitor.start();
        
        trainer=NoteTrainer()
        trainer.addNoteListener(nl)
        trainer.main(loader);
        
    except KeyboardInterrupt:
        colorWipe(npx, Color(0,0,0), 50)
        nl_monitor.stop()
