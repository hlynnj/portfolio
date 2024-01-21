import sys, os
sys.path.insert(0, os.path.abspath('..'))

from imslib.core import BaseWidget, run, lookup
from imslib.gfxutil import topleft_label, CEllipse, KFAnim, AnimGroup, CRectangle

from imslib.audio import Audio
from imslib.mixer import Mixer
from imslib.wavegen import WaveGenerator
from imslib.wavesrc import WaveBuffer, WaveFile

from player import PlayerGraphics
from tracks import TracksGraphics
from obstacle import Obstacle
from train import Train

from kivy.core.window import Window
from kivy.clock import Clock as kivyClock
from kivy.graphics import Color, Ellipse, Rectangle, Line

class MainWidget1(BaseWidget):
    def __init__(self):
        super(MainWidget1, self).__init__()

        self.audio = Audio(2)
        self.mixer = Mixer()
        self.audio.set_generator(self.mixer)
        self.mixer.set_gain(0.5)

        self.solo = WaveGenerator(WaveFile("../data/audio/test/KillerQueen_solo.wav"))
        self.mixer.add(self.solo)
        self.solo.pause()

        self.tracks = TracksGraphics()
        self.player = PlayerGraphics(self.tracks)
        self.objects = AnimGroup()

        self.objects.add(self.tracks)

        self.objects.add(self.player)
        self.canvas.add(self.objects)

        self.obstacles = [Obstacle(self.tracks, 0, 1), Obstacle(self.tracks, 1, 6.5), Obstacle(self.tracks, 2, 4)]
        for i in self.obstacles:
            self.canvas.add(i)

        self.trains = [Train(self.tracks, 0, 3, 5), Train(self.tracks, 1, 2, 2.5), Train(self.tracks, 2, 6, 7)]

        for i in self.trains:
            self.canvas.add(i)

        self.playing = False

    def on_resize(self, win_size):
        self.tracks.on_resize(win_size)
        for train in self.trains:
                train.on_resize(win_size)
        for obstacle in self.obstacles:
            obstacle.on_resize(win_size)
        self.player.on_resize(win_size)


    def on_key_down(self, keycode, modifiers):
        if keycode[1] == 'up':
            self.player.jump()
        if keycode[1] == 'right':
            self.player.switch_lanes(True)
        if keycode[1] == 'left':
            self.player.switch_lanes(False)
        if keycode[1] == 'p':
            self.tracks.start_anim()
            self.playing = True
            self.solo.play()
        if keycode[1] == 'q':
            self.tracks.switch_mode()
            for i in self.trains:
                i.switch_mode()
            for i in self.obstacles:
                i.switch_mode()
        

    def on_update(self):
        self.objects.on_update()
        self.audio.on_update()

        now_time = self.solo.frame / self.audio.sample_rate
        if self.playing:
            for obstacle in self.obstacles:
                obstacle.on_update(now_time)

        if self.playing:
            for train in self.trains:
                train.on_update(now_time)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f'run {sys.argv[0]} <num> to choose MainWidget<num>')
    else:
        run(eval('MainWidget' + sys.argv[1])())