import numpy
import math
from constants import NOTES

class NoteTrainer(object):
    def addNoteListener(self, noteListener):
        self.noteListener=noteListener
        
    def addSoundLevelListener(self,sll):
        self.sll=sll
        
    def __init__(self):
        self.noteListener=None
        self.tunerNotes = NOTES
        # Sort the keys and turn into a numpy array for logical indexing
        self.frequencies = numpy.array(sorted(self.tunerNotes.keys()))
        
    def main(self, loader):
        print("initiating vars ...")
        stepsize = 5
        
        tunerNotes=self.tunerNotes
        frequencies=self.frequencies

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
        soundgate = 17.5                            # zero is loudest possible input level
        targetnote=0
        print("initiating sound recorder ...")
        sound_recorder=SoundRecorder()                          # recording device (usb mic)
        print("sound_recorder intiated", trys)
        loader.stop()
        while True:
            try:
                sound_recorder.setup()
                raw_data_signal = sound_recorder.getAudio()
                signal_level = round(abs(loudness(raw_data_signal)),2)                  #### find the volume from the audio sample

                try:
                    fr=freq_from_autocorr(raw_data_signal,sound_recorder.RATE)
                    inputnote = round(fr,2)
                except Exception as e:
                    inputnote = 0
                    
                sound_recorder.close()

                if inputnote > frequencies[len(tunerNotes)-1]:                        #### not interested in notes above the notes list
                    continue

                if inputnote < frequencies[0]:                                     #### not interested in notes below the notes list
                    continue

                if signal_level > soundgate:
                    '''if self.sll != None:
                        self.sll.update(signal_level, None)      '''               #### basic noise gate to stop it guessing ambient noises
                    continue

                #print("frequence: ", inputnote, "Hz")
                #print("tuner note ", tunerNotes[frequencies[targetnote]])
                #print("signal level", signal_level)

                targetnote = closest_value_index(frequencies, round(inputnote, 2))
                
                ##### use the controls to make changes to the data #####
                print("level, freq, tuner_note, target_note", signal_level, str(inputnote)+"Hz", tunerNotes[frequencies[targetnote]], targetnote)
                if self.noteListener!=None:
                    self.noteListener.note(inputnote)
                
                '''if self.sll != None:
                    self.sll.update(signal_level, inputnote)'''

            except Exception as e:
                print(traceback.format_exc())


# See https://github.com/endolith/waveform-analyzer/blob/master/frequency_estimator.py
def freq_from_autocorr(raw_data_signal, fs):
    corr = fftconvolve(raw_data_signal, raw_data_signal[::-1], mode='full')
    #print(len(corr))
    corr = corr[int(math.floor(len(corr)/2)):]
    d = numpy.diff(corr)
    start = find(d > 0)[0]
    peak = numpy.argmax(corr[start:]) + start
    px, py = parabolic(corr, peak)
    return fs / px

# See https://github.com/endolith/waveform-analyzer/blob/master/frequency_estimator.py
def parabolic(f, x):
    xv = 1/2. * (f[x-1] - f[x+1]) / (f[x-1] - 2 * f[x] + f[x+1]) + x
    yv = f[x] - 1/4. * (f[x-1] - f[x+1]) * (xv - x)
    return (xv, yv)

def find(condition):
    res, = nonzero(ravel(condition))
    return res

def loudness(chunk):
    data = numpy.array(chunk, dtype=float) / 32768.0
    ms = math.sqrt(numpy.sum(data ** 2.0) / len(data))
    if ms < 10e-8: ms = 10e-8
    return 10.0 * math.log(ms, 10.0)

def closest_value_index(array, guessValue):
    # Find closest element in the array, value wise
    closestValue = find_nearest(array, guessValue)
    # Find indices of closestValue
    indexArray = numpy.where(array==closestValue)
    # Numpys 'where' returns a 2D array with the element index as the value
    return indexArray[0][0]
    
def find_nearest(array, value):
    index = (numpy.abs(array - value)).argmin()
    return array[index]
