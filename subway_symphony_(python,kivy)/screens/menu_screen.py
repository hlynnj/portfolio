import sys, os
sys.path.insert(0, os.path.abspath('..'))

from imslib.gfxutil import topleft_label, resize_topleft_label, CLabelRect, CRectangle
from imslib.screen import Screen

from imslib.wavegen import WaveGenerator
from imslib.wavesrc import WaveFile, WaveBuffer
from imslib.audio import Audio
from imslib.mixer import Mixer

from kivy.core.window import Window
from kivy.uix.button import Button
from kivy import metrics

from kivy.core.image import Image

font_sz = metrics.dp(20)
button_sz = metrics.dp(120)

class MenuScreen(Screen):
    def __init__(self, **kwargs):

        super(MenuScreen, self).__init__(always_update=False, **kwargs)

        self.audio = Audio(2)
        self.mixer = Mixer()
        self.audio.set_generator(self.mixer)

        self.trepak_audio = WaveGenerator(WaveFile('./data/audio/Nutcracker/Nutcracker_full.wav')) # need to change to full track
        self.trepak_audio.pause()
        self.mixer.add(self.trepak_audio)

        self.waltz_audio = WaveGenerator(WaveFile('./data/audio/Waltz/Waltz_full.wav')) # need to change to full track
        self.waltz_audio.pause()
        self.mixer.add(self.waltz_audio)

        self.button_width = button_sz * 2
        self.button_height = button_sz * 0.6

        self.trepak_left = Window.width*0.5-(self.button_width*0.5)
        self.trepak_right = Window.width*0.5+(self.button_width*0.5)
        self.trepak_top = Window.height*0.7+(self.button_height*0.5)
        self.trepak_bottom = Window.height*0.7-(self.button_height*0.5)

        self.trepak_button = Button(text='Trepak (Russian Dance)\n-Hard-', font_size=font_sz, size=(self.button_width, self.button_height), pos = (self.trepak_left, self.trepak_bottom), halign="center")
        self.trepak_button.background_color = [0.8, 0.8, 0.8, 1]
        self.trepak_button.bind(on_release= lambda x: self.switch_to('trepak'))

        self.add_widget(self.trepak_button)
        self.trepak_hover = False

        self.waltz_left = Window.width*0.5-(self.button_width*0.5)
        self.waltz_right = Window.width*0.5+(self.button_width*0.5)
        self.waltz_top = Window.height*0.5+(self.button_height*0.5)
        self.waltz_bottom = Window.height*0.5-(self.button_height*0.5)

        self.waltz_button = Button(text='Waltz of the Flowers\n-Easy-', font_size=font_sz, size=(self.button_width, self.button_height), pos = (self.waltz_left, self.waltz_bottom), halign="center")
        self.waltz_button.background_color = [0.8, 0.8, 0.8, 1]
        self.waltz_button.bind(on_release= lambda x: self.switch_to('waltz'))

        self.add_widget(self.waltz_button)
        self.waltz_hover = False

        self.tutorial_left = Window.width*0.5-(self.button_width*0.5)
        self.tutorial_right = Window.width*0.5+(self.button_width*0.5)
        self.tutorial_top = Window.height*0.3+(self.button_height*0.5)
        self.tutorial_bottom = Window.height*0.3-(self.button_height*0.5)

        self.tutorial_button = Button(text='Tutorial', font_size=font_sz, size=(self.button_width, self.button_height), pos=(self.tutorial_left, self.tutorial_bottom))
        self.tutorial_button.background_color = [0.8, 0.8, 0.8, 1]
        self.tutorial_button.bind(on_release= lambda x: self.switch_to('tutorial'))

        self.tutorial_hover = False

        self.add_widget(self.tutorial_button)

        Window.bind(mouse_pos=self.mouse_pos)

    
    def mouse_pos(self, window, pos):

        x = metrics.dp(pos[0])
        y = metrics.dp(pos[1])

        # trepak button hover
        if x > self.trepak_left and x < self.trepak_right and y > self.trepak_bottom and y < self.trepak_top:
            if not self.trepak_hover:
                self.trepak_audio.play()
                self.trepak_button.background_color = [0.5, 0.5, 0.5, 1]
                self.trepak_hover = True
        else:
            if self.trepak_hover:
                self.trepak_audio.pause()
                self.trepak_audio.reset()
                self.trepak_button.background_color = [0.8, 0.8, 0.8, 1]
                self.trepak_hover = False
        
        # waltz button hover
        if x > self.waltz_left and x < self.waltz_right and y > self.waltz_bottom and y < self.waltz_top:
            if not self.waltz_hover:
                self.waltz_audio.play()
                self.waltz_button.background_color = [0.5, 0.5, 0.5, 1]
                self.waltz_hover = True
        else:
            if self.waltz_hover:
                self.waltz_audio.pause()
                self.waltz_audio.reset()
                self.waltz_button.background_color = [0.8, 0.8, 0.8, 1]
                self.waltz_hover = False
        
        # tutorial button hover
        if x > self.tutorial_left and x < self.tutorial_right and y > self.tutorial_bottom and y < self.tutorial_top:
            if not self.tutorial_hover:
                self.tutorial_button.background_color = [0.5, 0.5, 0.5, 1]
                self.tutorial_hover = True
        else:
            if self.tutorial_hover:
                self.tutorial_button.background_color = [0.8, 0.8, 0.8, 1]
                self.tutorial_hover = False

    def on_update(self):
        self.audio.on_update()

    def on_resize(self, win_size):
        
        self.button_width = button_sz * 2
        self.button_height = button_sz * 0.6

        self.trepak_left = win_size[0]*0.5-(self.button_width*0.5)
        self.trepak_right = win_size[0]*0.5+(self.button_width*0.5)
        self.trepak_top = win_size[1]*0.7+(self.button_height*0.5)
        self.trepak_bottom = win_size[1]*0.7-(self.button_height*0.5)

        self.waltz_left = win_size[0]*0.5-(self.button_width*0.5)
        self.waltz_right = win_size[0]*0.5+(self.button_width*0.5)
        self.waltz_top = win_size[1]*0.55+(self.button_height*0.5)
        self.waltz_bottom = win_size[1]*0.55-(self.button_height*0.5)

        self.tutorial_left = win_size[0]*0.5-(self.button_width*0.5)
        self.tutorial_right = win_size[0]*0.5+(self.button_width*0.5)
        self.tutorial_top = win_size[1]*0.4+(self.button_height*0.5)
        self.tutorial_bottom = win_size[1]*0.4-(self.button_height*0.5)

        self.trepak_button.pos = (self.trepak_left, self.trepak_bottom)
        self.waltz_button.pos = (self.waltz_left, self.waltz_bottom)
        self.tutorial_button.pos = (self.tutorial_left, self.tutorial_bottom)