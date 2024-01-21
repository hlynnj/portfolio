import sys, os
sys.path.insert(0, os.path.abspath('....'))

from imslib.core import BaseWidget, run, lookup
from imslib.gfxutil import topleft_label

from logic import GemManager, MapManager, Player
from audio import AudioController
from improv import ImprovManager
from imslib.clock import SimpleTempoMap, Clock, Scheduler

from kivy.graphics import Line, InstructionGroup

class MainWidget(BaseWidget):

    def __init__(self):
        super(MainWidget, self).__init__()

        # self.gem_manager = GemManager('KillerQueen')
        self.gem_manager = GemManager('Nutcracker')
        self.map_manager = MapManager('Nutcracker')
        self.audio_ctrl = AudioController('./data/audio/Nutcracker/Nutcracker')
        self.improv_ctrl = ImprovManager(self.audio_ctrl)
        self.player = Player(gem_manager=self.gem_manager, map_manager=self.map_manager, audio_ctrl=self.audio_ctrl, improv_ctrl=self.improv_ctrl)

        # self.tempo_map = SimpleTempoMap(154)
        # self.clock = Clock()
        # self.sched = Scheduler(self.clock, self.tempo_map)

        self.info = topleft_label()
        self.add_widget(self.info)

        self.mode = 'reg' # 'reg' for regular, 'improv' for improv
    
    
    def on_key_down(self, keycode, modifiers):
        # play / pause toggle
        if keycode[1] == 'p':
            self.audio_ctrl.toggle()

            # now = self.sched.get_tick()
            # later = now + 960
            # self.sched.post_at_tick(self.player.change_mode, later)

        if keycode[1] == 'left' or keycode[1] == 'right' or keycode[1] == 'spacebar' or keycode[1] == 'up':
            self.player.on_player_action(keycode[1])
        
        # switch between improv and not improv
        if keycode[1] == 'm':
            self.player.change_mode()
    
    def on_update(self):

        self.audio_ctrl.on_update()
        # self.improv_ctrl.on_update()
        # self.sched.on_update()

        now = self.audio_ctrl.get_time()  # time of song in seconds.
        self.player.on_update(now)

        self.info.text = f'current lead lane = {self.player.lead_lane}\n'
        self.info.text += f'current player lane = {self.player.curr_lane}\n'
        self.info.text += f'current lead instrument = {self.player.lead_instr}\n'
        self.info.text += f'current mode = {self.player.mode}\n'

run(MainWidget())