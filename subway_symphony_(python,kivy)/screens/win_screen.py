import sys, os
sys.path.insert(0, os.path.abspath('..'))

from imslib.gfxutil import topleft_label, CLabelRect
from imslib.screen import Screen
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy import metrics

font_sz = metrics.dp(20)

class WinScreen(Screen):
    def __init__(self, **kwargs):
        super(WinScreen, self).__init__(**kwargs)

        self.score = None

        self.text1 = CLabelRect(cpos=(Window.width*0.5, Window.height*0.5), text="You win!", font_size=40, font_name='Gemstone.ttf')
        self.text2 = CLabelRect(cpos=(Window.width*0.5, Window.height*0.4), text="Score: ", font_size=21, font_name='Gemstone.ttf')

        self.canvas.add(self.text1)
        self.canvas.add(self.text2)

        self.button = Button(text='Return To Menu', font_size=font_sz, size = (Window.width*0.2, Window.height*0.1), pos = (Window.width*0.4, Window.height*0.2))
        self.button.bind(on_release= lambda x: self.switch_to('menu'))

        self.add_widget(self.button)
    
    def set_score(self, score):

        self.score = score
        print(self.score)
        self.text2.set_text(f"Score: {self.score}")
    
    def on_key_down(self, keycode, modifiers):
        pass

    def on_resize(self, win_size):
        self.text1.set_cpos(cpos=(win_size[0]*0.5, win_size[1]*0.5))
        self.text2.set_cpos(cpos=(win_size[0]*0.5, win_size[1]*0.4))
        self.button.pos = (win_size[0]*0.4, win_size[1]*0.2)
        self.button.size = (win_size[0]*0.2, win_size[1]*0.1)