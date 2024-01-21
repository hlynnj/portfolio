import sys, os
sys.path.insert(0, os.path.abspath('..'))

from imslib.gfxutil import topleft_label, resize_topleft_label, CLabelRect, CRectangle
from imslib.screen import Screen
from kivy.core.image import Image

from kivy.core.window import Window
from kivy.uix.button import Button
from kivy import metrics

font_sz = metrics.dp(20)

class TutorialScreen(Screen):
    def __init__(self, **kwargs):
        super(TutorialScreen, self).__init__(always_update=False, **kwargs)

        self.screen_title = CLabelRect(cpos=(Window.width/2, Window.height*0.85), text="Tutorial", font_size=35, font_name='Gemstone.ttf')

        self.image_1 = CRectangle(cpos = (Window.width*0.88, Window.height*0.65), csize=(Window.width*0.05, Window.width*0.11), texture=Image('./data/images/nutcracker/nutcracker_full.png').texture)

        text_1 = "You Control The Nutcracker"
        self.text_1 = CLabelRect(cpos = (Window.width*0.67, Window.height*0.65), text=text_1, font_name="Gemstone.ttf", font_size=25)

        self.image_2 = CRectangle(cpos = (Window.width*0.27, Window.height*0.45), csize=(Window.width*0.35, Window.width*0.45), texture=Image('./data/images/intro/tutorial_1.png').texture)

        text_2 = "Avoid Obstacles By Changing\nLanes With Left / Right Arrows \nAnd Jumping With Up Arrow"
        self.text_2 = CLabelRect(cpos = (Window.width*0.7, Window.height*0.50), text=text_2, font_name="Gemstone.ttf", font_size=25)

        self.image_3 = CRectangle(cpos = (Window.width * 0.88, Window.height*0.3), csize=(Window.width*0.07, Window.width*0.07), texture=Image('./data/images/coins/horn.png').texture)

        text_3 = "Press Space Along With Music\n To Collect Instrument Coins\n And Play That Instrument!"
        self.text_3 = CLabelRect(cpos = (Window.width*0.67, Window.height*0.3), text=text_3, font_name='Gemstone.ttf', font_size=25)
    
        self.page_number_1 = CLabelRect(cpos=(Window.width*0.9, Window.height*0.1), text="1/2", font_name='Gemstone.ttf')

        text_4 = "Click To Next Page"
        self.text_4 = CLabelRect(cpos = (Window.width*(3/4), Window.height*0.1), text=text_4, font_name="Gemstone.ttf", font_size=21)

        self.canvas.add(self.screen_title)

        self.objects1 = [self.image_1, self.text_1, self.image_2, self.text_2, self.image_3, self.text_3, self.text_4, self.page_number_1]

        for obj in self.objects1:
            self.canvas.add(obj)
        

        """
        When You Collect The Yellow Improv Token,
        You Enter Improv Mode, Where You 
        Control An Instrument!
        Press Space To Play Your Instrument
        However You Would Like To Play It!
        The Game Will Remember Your Playing
        And Play It Back To You.
        """
        self.image_4 = CRectangle(cpos = (Window.width*0.27, Window.height*0.45), csize=(Window.width*0.35, Window.width*0.53), texture=Image('./data/images/intro/tutorial_2.png').texture)

        text_5 = "When You Collect \nThe Golden Token,\nYou Enter Improv Mode, Where You\nControl An Instrument!\nPress Space To Play Your Instrument\nHowever You Would Like To Play It!\nThe Game Will Remember Your Playing\nAnd Play It Back To You."
        self.text_5 = CLabelRect(cpos = (Window.width*0.75, Window.height*0.5), text=text_5, font_name="Gemstone.ttf", font_size=25)

        self.image_5 = CRectangle(cpos = (Window.width*0.80, Window.height*0.65), csize=(Window.width*0.1, Window.width*0.1), texture=Image('./data/images/tokens/tambourine_gold.png').texture)

        self.page_number_2 = CLabelRect(cpos=(Window.width*0.9, Window.height*0.1), text="2/2", font_name='Gemstone.ttf')

        text_6 = "Return To Menu"
        self.text_6 = CLabelRect(cpos = (Window.width*(3/4), Window.height*0.1), text=text_6, font_name="Gemstone.ttf", font_size=21)

        self.objects2 = [self.image_4, self.text_5, self.image_5, self.page_number_2, self.text_6]

        self.current_page = 1
    
    def on_enter(self):

        if self.current_page == 2:
            for obj in self.objects2:
                self.canvas.remove(obj)
            for obj in self.objects1:
                self.canvas.add(obj)
            self.current_page = 1

    def on_touch_down(self, touch):
        
        if self.current_page == 1:
            self.current_page = 2
            for obj in self.objects1:
                self.canvas.remove(obj)
            for obj in self.objects2:
                self.canvas.add(obj)
        elif self.current_page == 2:
            self.switch_to('menu')
    
    def on_resize(self, win_size):

        self.screen_title.set_cpos((win_size[0]*0.5, win_size[1]*0.85))

        self.image_1.set_cpos((win_size[0]*0.88, win_size[1]*0.65))
        self.image_1.set_csize((win_size[0]*0.05, win_size[0]*0.11))

        self.text_1.set_cpos((win_size[0]*0.67, win_size[1]*0.65))

        self.image_2.set_cpos((win_size[0]*0.27, win_size[1]*0.45))
        self.image_2.set_csize((win_size[0]*0.35, win_size[0]*0.45))

        self.text_2.set_cpos((win_size[0]*0.7, win_size[1]*0.5))

        self.image_3.set_cpos((win_size[0]*0.88, win_size[1]*0.3))
        self.image_3.set_csize((win_size[0]*0.07, win_size[0]*0.07))

        self.text_3.set_cpos((win_size[0]*0.67, win_size[1]*0.3))

        self.page_number_1.set_cpos((win_size[0]*0.9, win_size[1]*0.1))

        self.image_4.set_cpos((win_size[0]*0.27, win_size[1]*0.45))
        self.image_4.set_csize((win_size[0]*0.35, win_size[0]*0.53))

        self.text_4.set_cpos((win_size[0]*0.75, win_size[1]*0.1))

        self.text_5.set_cpos((win_size[0]*0.75, win_size[1]*0.5))

        self.image_5.set_cpos((win_size[0]*0.8, win_size[1]*0.65))
        self.image_5.set_csize((win_size[0]*0.1, win_size[0]*0.1))

        self.page_number_2.set_cpos((win_size[0]*0.9, win_size[1]*0.1))

        self.text_6.set_cpos((win_size[0]*0.75, win_size[1]*0.1))

    def on_update(self):
        pass
