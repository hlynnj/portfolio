from imslib.audio import Audio
from imslib.mixer import Mixer
from imslib.wavegen import WaveGenerator
from imslib.wavesrc import WaveFile, WaveBuffer
from imslib.synth import Synth
from imslib.clock import SimpleTempoMap, AudioScheduler, kTicksPerQuarter, quantize_tick_up
from imslib.metro import Metronome

# NOTE:
# (1) clarify what the user should be doing
# (2) can't really force user to improv?
# (3) hook graphics up to sound, graphical support for playback


######################
##    DEPRECATED    ##
######################

class ImprovManager(object):

    def __init__(self, background_audio):

        super(ImprovManager, self).__init__()

        # parameters
        self.start_delay_ticks = 480

        self.tick_since_last_incr = 0
        self.min_tick_spacing = 240
        self.notes_in_loop = 2 * 4 * 2 # 4 measures, 4 beats, eights each
        self.num_loops = 3
        self.loop_idx = 0
        self.play_prev = False
        self.last_input_tick = self.min_tick_spacing

        # audio
        self.tempo_map = SimpleTempoMap(77)
        self.audio = Audio(2)
        self.synth = Synth()

        # hooking audio up
        self.main_sched = AudioScheduler(self.tempo_map)
        self.audio.set_generator(self.main_sched)
        self.main_sched.set_generator(self.synth)
        self.cmd = None

        # instruments for each loop
        self.synth.program(0, 128, 0)
        self.synth.program(1, 128, 0)
        self.synth.program(2, 128, 0)
        # (1) tambourine (2) low floor tom (3) crash cymbal
        self.instruments = {0: 54, 1: 41, 2: 49}

        # needs to be the audio controller object from player
        self.background_audio = background_audio

        # note_idx control
        self.notes = {}
        for i in range(self.num_loops):
            self.notes[i] = [False for _ in range(self.notes_in_loop)]
        self.note_idx = 0

        # game logic
        self.current_lane = 1

        # callback exiting improv mode
        self.end_callback = None # should be set using the setter function!

        # callback to change improv text (instructions)
        self.text_change_callback = None # should be set using the setter function!

    # schedules initial improv commands
    def start(self):

        # print('starting')

        if not self.end_callback or not self.text_change_callback:
            print("make sure you set the callback!")
            return
        
        self.change_improv_text()
        # starts incrementing note_idx to keep track of input + playback
        now = self.main_sched.get_tick()
        next_beat = quantize_tick_up(now + self.start_delay_ticks, 480)
        self.cmd = self.main_sched.post_at_tick(self._start_improv, next_beat)
    
    def stop(self):

        # called by itself at the end of improv mode

        # print('stopping')
        self.background_audio.toggle()

        self.main_sched.cancel(self.cmd)
        self.cmd = None

        self.end_callback() # note: makesure this callback doesn't call this function again!
    
    def set_end_callback(self, callback):
        self.end_callback = callback
    
    def change_player_lane(self, new_lane):
        # called by logical player to keep track of player lane
        self.current_lane = new_lane
    
    def set_text_change_callback(self, callback):
        self.text_change_callback = callback
    
    def change_improv_text(self):
        # callback should be the set_improv_text function in game_display
        lane = self.loop_idx

        if self.loop_idx == 0:
            instrument = "tambourine"
        elif self.loop_idx == 1:
            instrument = "drums"
        elif self.loop_idx == 2:
            instrument = "cymbals"
        else:
            instrument = ""

        self.text_change_callback(lane, instrument)
    

    # takes in player input
    def on_tap(self):

        # print('pressed')

        if self.num_loops < self.loop_idx:
            return
        
        # only play MIDI notes if user is in correct lane
        if self.current_lane != self.loop_idx:
            if self.note_idx != 0:
                return
            
        now = self.main_sched.get_tick()

        # necessary step due to how note_idx is incremented
        if self.note_idx - 1 < 0 and self.loop_idx > 0:
            loop_idx = self.loop_idx - 1
            note_idx = len(self.notes[0]) - 1
        else:
            loop_idx = self.loop_idx
            note_idx = max(0, self.note_idx -1)
            
        print("tapped for note ", loop_idx, note_idx)

        # select corresponding note as "played"
        # case: regular
        if not self.notes[loop_idx][note_idx]:
            self.last_input_tick = now
            self._noteon(now, (loop_idx, self.instruments[loop_idx]))
            self.notes[loop_idx][note_idx] = True
        # case: early for next note
        elif (now - self.last_input_tick) > (self.min_tick_spacing * 0.9):
            self.last_input_tick = now
            self._noteon(now, (loop_idx, self.instruments[loop_idx]))
            self.notes[loop_idx][note_idx + 1] = True

        
    def _noteon(self, tick, params):

        # turns synth note on, schedules note off
        chan = params[0]
        key = params[1]

        self.synth.noteon(chan, key, 100)
        self.main_sched.post_at_tick(self._noteoff, tick+480, (chan, key))


    def _noteoff(self, tick, params):

        # turns synth note off
        chan = params[0]
        key = params[1]

        self.synth.noteoff(chan, key)


    def _start_improv(self, tick):

        # called by self.start at the actual beginning of improv
        self.background_audio.toggle()
        self._increment_note_idx(tick)


    def _increment_note_idx(self, tick):
        # increments note_idx, plays back prev user input if applicable
        
        print(self.note_idx)
        # print("incrementing at loop ", self.loop_idx)

        if self.play_prev:
            for i in range(self.loop_idx):
                if self.notes[i][self.note_idx]:
                    print("replaying note from ", i, " ", self.note_idx)
                    self._noteon(tick, (i, self.instruments[i]))

        # increment note_idx
        self.note_idx += 1

        # at the end of the loop
        if self.note_idx == len(self.notes[0]):
            self.loop_idx += 1
            self.play_prev = True
            self.note_idx = 0
            self.change_improv_text()
        # at the end of improv
        if self.loop_idx > self.num_loops:
            self.stop()
            self.change_improv_text()
            return

        # schedule next increment
        next_beat = quantize_tick_up(tick, self.min_tick_spacing)
        self.cmd = self.main_sched.post_at_tick(self._increment_note_idx, next_beat)

    
    def on_update(self):

        self.audio.on_update()
        self.background_audio.on_update()