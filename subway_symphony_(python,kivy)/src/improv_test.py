import sys, os
sys.path.insert(0, os.path.abspath('....'))

from imslib.core import BaseWidget, run, lookup
from imslib.gfxutil import topleft_label

from imslib.audio import Audio

from imslib.clock import SimpleTempoMap, Clock, Scheduler

from src.improv import ImprovManager

class MainWidget(BaseWidget):

    def __init__(self):
        super(MainWidget, self).__init__()

        self.improv_manager = ImprovManager()

        self.info = topleft_label()
        self.add_widget(self.info)
    
    def on_key_down(self, keycode, modifiers):
        # start improv
        if keycode[1] == 'i':
            self.improv_manager.start()

        # play / pause toggle
        if keycode[1] == 'spacebar':
            self.improv_manager.on_tap()
    
    def on_update(self):
        self.info.text = f'audio load: {self.improv_manager.audio.get_cpu_load():.2f}\n'
        self.improv_manager.on_update()

run(MainWidget())