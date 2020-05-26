import numpy
from utils import closest_value_index, freq_from_autocorr, loudness
from constants import NOTES
from sound_recorder import SoundRecorder


class NoteTrainer(object):
    def addNoteListener(self, noteListener):
        self.noteListener=noteListener;
        
    def __init__(self):
        self.noteListener=None    
        self.tunerNotes = NOTES
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
        sound_recorder = SoundRecorder()                          # recording device (usb mic)
        print("sound_recorder intiated", trys);
        loader.stop();
        while True:
            sound_recorder.setup()
            raw_data_signal = sound_recorder.getAudio()
            signal_level = round(abs(loudness(raw_data_signal)),2)                  #### find the volume from the audio sample

            try:
                fr = freq_from_autocorr(raw_data_signal,sound_recorder.RATE);
                inputnote = round(fr,2)
            except Exception as e:
                inputnote = 0
                
            sound_recorder.close()

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

            ####### Draw Stuff on the screen #######

            # display note names if selected
            if shownotes:
                print("signal_level", signal_level)
                err = abs(frequencies[targetnote]-inputnote)
                print("note & err", tunerNotes[frequencies[targetnote]], err)
