import pyaudio
import numpy


# See http://www.swharden.com/blog/2013-05-09-realtime-fft-audio-visualization-with-python/
class SoundRecorder:
    def __init__(self):
        self.RATE = 44100
        self.BUFFERSIZE = 1024 #1024 is a good buffer size 3072 works for Pi
        self.secToRecord = .05
        self.threadsDieNow = False
        self.newAudio = False

        p = pyaudio.PyAudio()
        print("scanning input devices ...")

        self.device_index=0

        for i in range(p.get_device_count()):
            dev = p.get_device_info_by_index(i)
            print((i,dev['name'],dev['maxInputChannels']))
            if 'USB' in dev['name']:
                self.device_index=i

        print("Using device no ", self.device_index)

    def setup(self):
        self.buffersToRecord = int(self.RATE*self.secToRecord/self.BUFFERSIZE)
        if self.buffersToRecord == 0 : self.buffersToRecord = 1
        self.samplesToRecord = int(self.BUFFERSIZE*self.buffersToRecord)
        self.chunksToRecord = int(self.samplesToRecord/self.BUFFERSIZE)
        self.secPerPoint = 1.0/self.RATE
        self.pyaudio = pyaudio.PyAudio()
        self.inStream = self.pyaudio.open(input_device_index=self.device_index, format=pyaudio.paInt16,channels=1,rate=self.RATE,input=True,frames_per_buffer=self.BUFFERSIZE)
        self.xsBuffer = numpy.arange(self.BUFFERSIZE)*self.secPerPoint
        self.xs = numpy.arange(self.chunksToRecord*self.BUFFERSIZE) * self.secPerPoint
        self.audio = numpy.empty((self.chunksToRecord*self.BUFFERSIZE), dtype=numpy.int16)


    def close(self):
        self.pyaudio.close(self.inStream)

    def getAudio(self):
        audioString = self.inStream.read(self.BUFFERSIZE)
        self.newAudio = True
        return numpy.fromstring(audioString,dtype=numpy.int16)