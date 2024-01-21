import sys, os
sys.path.insert(0, os.path.abspath('..'))

from imslib.gfxutil import topleft_label, resize_topleft_label, CLabelRect, CRectangle
from imslib.screen import Screen

from kivy.core.window import Window
from kivy.uix.button import Button
from kivy import metrics

from kivy.core.image import Image

font_sz = metrics.dp(20)
button_sz = metrics.dp(100)

class IntroScreen(Screen):
    def __init__(self, **kwargs):

        super(IntroScreen, self).__init__(always_update=False, **kwargs)

        self.logo = CRectangle(cpos=(Window.width/2, Window.height/2), texture=Image('./data/images/intro/logo.png').texture, csize=(Window.width*0.8, Window.height*0.7*0.8))

        self.text = CLabelRect(cpos=(Window.width/2, Window.height*0.20), text="Click To Menu", font_size=Window.height/25, font_name='Gemstone.ttf')

        self.canvas.add(self.logo)
        self.canvas.add(self.text)
    
    def on_touch_down(self, touch):

        self.switch_to('menu')

    def on_update(self):
        pass

    def on_resize(self, win_size):
        self.logo.set_cpos((win_size[0]/2, win_size[1]/2))
        self.logo.set_csize((win_size[0]*0.8, win_size[1]*0.8*0.7))
        self.text.set_cpos((win_size[0]/2, win_size[1]*0.20))
        self.text.set_font_size(win_size[1]/25)