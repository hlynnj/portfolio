import sys, os
import re
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('./graphics'))

from imslib.gfxutil import topleft_label, CEllipse, AnimGroup, CLabelRect
from imslib.screen import Screen

from kivy.core.window import Window
from kivy.uix.button import Button
from kivy import metrics

from src.logic import GemManager, MapManager, Player
from src.audio import AudioController

from graphics.player import PlayerGraphics
from graphics.tracks import TracksGraphics
from graphics.obstacle import Obstacle
from graphics.coin import Coin

class SongData(object):
    def __init__(self, map_filepath, gems_filepath):
        super(SongData, self).__init__()

        # mapping is formatted as (time, lane, new_instr)
        self.mapping = self.create_mapping(map_filepath)

        # gems are formatted as (time, is_jump, lane, instrument)
        self.gems = self.create_gems(gems_filepath)

        self.obstacle_data, self.coin_data, self.train_data = self.create_data()

    def map_from_line(self, line):
        time, lane, instrument = re.split(';|\t', line.strip())
        return (float(time), int(lane), instrument)
    
    def create_mapping(self, filename):
        return [self.map_from_line(l) for l in open(filename).readlines()]
    
    def gem_from_line(self, line):
        time, is_jump, lane, instrument = re.split(';|\t', line.strip())
        return (float(time), bool(int(is_jump)), int(lane), instrument)
    
    def create_gems(self, filename):
        return [self.gem_from_line(l) for l in open(filename).readlines()]
    
    def create_data(self):
        ob = []
        c = []
        tr = []
        previous_lane = None
        for time, is_jump, lane, instrument in self.gems:
            if is_jump: # is_jump
                ob.append((lane, time))
            else:
                c.append((lane, time, instrument))

            if previous_lane is None: # add initial trains
                tr.append((0, 1, 2.5))
                tr.append((2, 2.5, 3))
            elif lane != previous_lane: # add train to make player switch
                tr.append((previous_lane, time + 0.5, time + 2))

            previous_lane = lane
            
        return ob, c, tr

    def get_gems(self):
        return self.gems

    def get_obstacle_data(self):
        return self.obstacle_data
    
    def get_coin_data(self):
        return self.coin_data
    
    def get_train_data(self):
        return self.train_data
    