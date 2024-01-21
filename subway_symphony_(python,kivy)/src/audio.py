from imslib.audio import Audio
from imslib.mixer import Mixer
from imslib.wavegen import WaveGenerator
from imslib.wavesrc import WaveFile, WaveBuffer
from imslib.synth import Synth
from imslib.clock import SimpleTempoMap, AudioScheduler, kTicksPerQuarter, quantize_tick_up
from imslib.metro import Metronome

####################
#   AudioManager   #
####################

# Keeps track of all audio files, their mute/unmutes, times, and volume

# Assets: - WavePlayer for each instrument track

# Functions:
# (1) set gain for specific instrument track
# (2) get song time from one of the tracks (probably one that never gets player control)

class AudioController(object):
    def __init__(self, piece, file_path):
        super(AudioController, self).__init__()
        # self.audio = Audio(2)
        # self.mixer = Mixer()

        self.piece = piece

        self.start_counter = 0 # count down from 3
        if self.piece == "Trepak":
            tempo = 77
        elif self.piece == "Waltz":
            tempo = 200
        self.tempo_map = SimpleTempoMap(tempo)
        self.audio = Audio(2)
        self.mixer = Mixer()
        self.synth = Synth()
        self.synth.program(0, 128, 0) # metronome
        self.synth.program(1, 128, 0) # user input during improv
        self.sched = AudioScheduler(self.tempo_map)
        self.metronome = Metronome(self.sched, self.synth)
        self.audio.set_generator(self.sched)
        self.sched.set_generator(self.mixer)
        self.mixer.add(self.synth)

        self.cmd = None

        self.mode = 'reg' # 'reg' for regular, 'improv' for improv

        # regular stuff
        if self.piece == "Trepak":
            self.instruments = ['bass', 'bassclarinet', 'bassoon', 'cello', 'clarinet', 'englishhorn', 'flute', 'horn', 'oboe', 'timpani', 'trombone', 'trumpet', 'tuba', 'viola', 'violin']
        elif self.piece == "Waltz":
            self.instruments = ['bass', 'bassoon', 'cello', 'clarinet', 'flute', 'harp', 'horn', 'oboe', 'timpani', 'triangle', 'trombone', 'trumpet', 'tuba', 'viola', 'violin']
        self.lead_instrument = 'violin' if self.piece == "Trepak" else 'bass'

        self.tracks = {}
        for instrument in self.instruments:
            file_name = file_path + "_" + instrument + ".wav"
            track = WaveGenerator(WaveFile(file_name))
            # start tracks paused
            track.pause()
            self.tracks[instrument] = track
            self.mixer.add(track)
        
        self.waiting = False

        # improv stuff

        if self.piece == "Trepak":
            self.improv_length = 2 * 4 * 2 # 2 measures, 4 beats, 2 notes each
        elif self.piece == "Waltz":
            self.improv_length = 8 * 3 * 1 # 8 measures, 3 beats, 1 note each
        self.tick_since_last_incr = 0

        if self.piece == "Trepak":
            self.min_tick_spacing = 240
        elif self.piece == "Waltz":
            self.min_tick_spacing = 480
        self.last_input_tick = self.min_tick_spacing
        self.playback = False # switched to true after 1 iteration of improv

        self.improv_instrument = 54 # tambourine
        self.notes = [False for _ in range(self.improv_length)]

        if self.piece == "Trepak":
            self.note_idx = self.improv_length - 6 - 1 # account for 6 beat delay
        if self.piece == "Waltz":
            self.note_idx = self.improv_length - (6*3) - 1 # account for 9 beat delay + intro measures

        self.improv_cycled = False

        # callback exiting improv mode, if any
        self.improv_end_callback = None # should be set using the setter function!

        # miss sound
        self.miss = WaveGenerator(WaveFile('./data/audio/sounds/miss.wav'))
        self.mixer.add(self.miss)
        self.miss.reset()
        self.miss.pause()

        # hitting side of train sound
        self.side_train = WaveGenerator(WaveFile('./data/audio/sounds/side_train.wav'))
        self.mixer.add(self.side_train)
        self.side_train.reset()
        self.side_train.pause()

    ##################
    #   Game Start   #
    ##################

    # called by game screen
    def toggle(self):

        # for instrument in self.tracks:
        #     self.tracks[instrument].play_toggle()

        now = self.sched.get_tick()
        self._decrement_start_counter(now)
    
    # count down to start
    def _decrement_start_counter(self, tick):
        self.waiting = True
        if self.start_counter == 0:
            self._start(tick)
        else:
            now = self.sched.get_tick()
            next_beat = quantize_tick_up(now + 480, 480)
            self.sched.post_at_tick(self._decrement_start_counter, next_beat)
            self.start_counter -= 1
    
    # actual start
    def _start(self, tick):
        self.waiting=False
        for instrument in self.tracks:
            self.tracks[instrument].play_toggle()
        # self.metronome.start()
        self._increment_note_idx(tick)
        # self.metronome.start()

    ################
    #   Game End   #
    ################

    # called by game screen at the end of the game
    # TODO: hook this up to player once game over logic is made
    def reset(self):
        for instrument in self.tracks:
            self.tracks[instrument].reset()
    
    # when game over, pause all the instruments
    def on_game_over(self):
        for instrument in self.tracks:
            self.tracks[instrument].reset()
            self.tracks[instrument].pause()

    #########################
    #   Getters & Setters   #
    #########################

    def get_instruments(self):
        return self.instruments
    
    # mute / unmute specific instruments
    def set_gain(self, instrument, gain):
        self.tracks[instrument].set_gain(gain)

    # return current time (in seconds) of song
    def get_time(self):
        return self.tracks['bass'].frame / Audio.sample_rate
    
    def get_frame(self):
        return self.tracks['bass'].frame

    def set_improv_end_callback(self, callback):
        self.improv_end_callback = callback
    
    #############################
    #   Regular Mode Controls   #
    #############################
    def on_lead_change(self, lead_instrument):

        for instrument in self.instruments:
            self.tracks[instrument].set_gain(0.2)
        self.tracks[lead_instrument].set_gain(1)
        self.lead_instrument = lead_instrument

    def play_miss(self):
        self.miss.reset()
        self.miss.play()

    def play_side_train(self):
        self.side_train.reset()
        self.side_train.play()

    ############################
    #   Improv Mode Controls   #
    ############################
    def start_improv(self):
        self.mode = 'improv'
        # return
        for instrument in self.instruments:
            self.tracks[instrument].set_gain(1)
        print(self.note_idx)
    
    def end_improv(self):
        self.mode = 'reg'
        self.improv_end_callback()
        
    def start_playback(self):
        self.playback = True

    def stop_playback(self, tick): # schedule end of playback to after 1 loop
        self.playback = False

    def on_tap(self):
        # respond to user input during improv

        if self.mode == 'reg' and self.note_idx != 0:
            print("cannot accept input during regular mode")
            return 
        
        now = self.sched.get_tick()

        # print(quantize_tick_up(now, self.min_tick_spacing) - now)

        # note_idx = max(0, self.note_idx-1)
        note_idx = self.note_idx

        # case: late hit
        if (quantize_tick_up(now, self.min_tick_spacing) - now > self.min_tick_spacing * 0.5):
            self.last_input_tick = now
            self._noteon(now)
            self.notes[note_idx] = True
            print("late tapped for note ", note_idx)
        # # case: early hit
        # elif (quantize_tick_up(now, self.min_tick_spacing) - now < self.min_tick_spacing * 0.4):
        #     self.last_input_tick = now
        #     self._noteon(now)
        #     self.notes[note_idx + 1] = True
        #     print("early tapped for note ", note_idx + 1)
    
    def _noteon(self, tick):

        self.synth.noteon(1, self.improv_instrument, 100)
        self.sched.post_at_tick(self._noteoff, tick+480)
    
    def _noteoff(self, tick):

        self.synth.noteoff(1, self.improv_instrument)
    
    def _increment_note_idx(self, tick):
        # increments note_idx and plays back previous user input if applicable

        # print(self.note_idx)

        # (2) increment note_idx
        self.note_idx += 1

        # (1) playback
        if self.playback:
            if self.note_idx < len(self.notes) and (self.notes[self.note_idx] or (self.note_idx == 0 and self.notes[-1])):
                print("replaying note ", self.note_idx)
                self._noteon(tick)
    
        # (3) at the end of the loop
        if self.mode == "improv" and self.note_idx == len(self.notes):
            self.note_idx = 0
            if self.improv_cycled:
                self.playback = True
                self.end_improv()
                # schedule end of playback
                self.sched.post_at_tick(self.stop_playback, tick+((self.improv_length+1)*self.min_tick_spacing))
        elif self.mode == "improv" and self.note_idx == int(0.5 * len(self.notes)):
            self.improv_cycled = True
        if self.note_idx == len(self.notes):
            self.note_idx = 0
        # print(self.note_idx)
        # (4) schedule next increment
        next_beat = quantize_tick_up(tick, self.min_tick_spacing)
        self.sched.post_at_tick(self._increment_note_idx, next_beat)

    # needed to update audio
    def on_update(self):
        self.audio.on_update()

        # re-add miss sound if it is removed
        if self.miss not in self.mixer.generators:
            self.mixer.add(self.miss)
            self.miss.reset()
            self.miss.pause()

        # re-add side train sound if it is removed
        if self.side_train not in self.mixer.generators:
            self.mixer.add(self.side_train)
            self.side_train.reset()
            self.side_train.pause()