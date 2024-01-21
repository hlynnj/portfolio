import sys, os
sys.path.insert(0, os.path.abspath('..'))

from imslib.gfxutil import topleft_label, CLabelRect
from imslib.screen import Screen
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy import metrics

font_sz = metrics.dp(20)

class EndScreen(Screen):
    def __init__(self, **kwargs):
        super(EndScreen, self).__init__(**kwargs)

        self.score = None

        self.text1 = CLabelRect(cpos=(Window.width*0.5, Window.height*0.5), text="Game Over", font_size=Window.height/20, font_name='Gemstone.ttf')
        self.text2 = CLabelRect(cpos=(Window.width*0.5, Window.height*0.43), text=f"Watch Out For Obstacles!", font_size=Window.height/35, font_name='Gemstone.ttf')

        self.text3 = CLabelRect(cpos=(Window.width*0.5, Window.height*0.38), text=f"Score: {self.score}", font_size=Window.height/35, font_name='Gemstone.ttf')

        self.canvas.add(self.text1)
        self.canvas.add(self.text2)
        self.canvas.add(self.text3)

        self.button = Button(text='Restart Game', font_size=font_sz, size = (Window.width*0.2, Window.height*0.1), pos = (Window.width*0.4, Window.height*0.2))
        self.button.bind(on_release= lambda x: self.switch_to('menu'))

        self.add_widget(self.button)

    def on_key_down(self, keycode, modifiers):
        pass

    def set_score(self, score):

        self.score = score
        print(self.score)
        self.text3.set_text(f"Score: {self.score}")

    def on_resize(self, win_size):
        self.text1.set_cpos(cpos=(win_size[0]*0.5, win_size[1]*0.5))
        self.text1.set_font_size(win_size[1]/20)
        self.text2.set_cpos(cpos=(win_size[0]*0.5, win_size[1]*0.43))
        self.text2.set_font_size(win_size[1]/35)
        self.text3.set_font_size(win_size[1]/35)
        self.text3.set_cpos(cpos=(win_size[0]*0.5, win_size[1]*0.38))
        self.button.pos = (win_size[0]*0.4, win_size[1]*0.2)
        self.button.size = (win_size[0]*0.2, win_size[1]*0.1)