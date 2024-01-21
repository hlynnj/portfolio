from imslib.gfxutil import topleft_label, CEllipse, KFAnim, AnimGroup, CRectangle, CLabelRect

from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Rectangle, Line, Quad
from kivy.graphics import PushMatrix, PopMatrix, Translate, Scale, Rotate
from kivy.core.image import Image

from helper_funcs import *

height_to_width_ratio = 0.2
initial_size_multiplier = 1/70
max_size_multiplier = 1/15
shadow_ypos_radius_multiplier = 0.4
shadow_x_size_multiplier = 1.25
shadow_y_size_multiplier = 0.5
instrument_paths = {
    'violin': './data/images/coins/violin.png',
    'clarinet': './data/images/coins/clarinet.png',
    'englishhorn': './data/images/coins/englishhorn.png',
    'flute': './data/images/coins/flute.png',
    'horn': './data/images/coins/horn.png',
    'bassclarinet': './data/images/coins/bassclarinet.png',
    'bassoon': './data/images/coins/bassoon.png',
    'cello': './data/images/coins/cello.png',
    'trombone': './data/images/coins/trombone.png',
    'viola': './data/images/coins/viola.png',
    'tuba': './data/images/coins/tuba.png',
    'trumpet': './data/images/coins/trumpet.png',
    'bass': './data/images/coins/bass.png',
    'harp': './data/images/coins/harp.png',
    'oboe': './data/images/coins/oboe.png'
}

class Coin(InstructionGroup):
    
    def __init__(self, tracks, lane, time, instrument):
        super(Coin, self).__init__()
        
        # coin variables
        self.tracks = tracks
        self.lane = lane
        self.time = time            # time in the song that the coin should be in the nowbar
        self.instrument = instrument

        # location/dimensions of the coin
        self.x_pos = self.tracks.get_lane_center_x(self.lane)               # start in middle of lane
        self.y_pos = Window.height                                          # start at top of screen
        self.initial_size = Window.height * initial_size_multiplier
        self.max_size = Window.height * max_size_multiplier
        self.radius = abs((Window.height - self.y_pos) / Window.height * (self.max_size - self.initial_size) + self.initial_size)
        
        # the x,y coordinates on the screen
        self.cbpos = map_coords_3D_to_2D(self.x_pos, self.y_pos, 0)
        self.csize = (self.radius, self.radius)

        # the coin drawing - a CEllipse
        self.image_path = instrument_paths[self.instrument]
        self.coin = CBEllipse(cbpos=self.cbpos, cbsize=self.csize, texture=Image(self.image_path).texture)
        self.shadow = CBEllipse(cbpos=(self.cbpos[0], self.cbpos[1] - self.radius * shadow_ypos_radius_multiplier), cbsize=(self.csize[0] * shadow_x_size_multiplier, self.csize[1] * shadow_y_size_multiplier))

        self.color = Color(1, 1, 0)
        self.add(self.color)
        self.add(self.coin)

        self.shadow_color = Color(0, 0, 0)
        self.shadow_color.a = 0.25
        self.add(self.shadow_color)
        self.add(self.shadow)

        self.hit = False
        self.just_hit = False
        self.passed = False

    def get_lane(self):
        return self.lane

    def get_y_pos(self):
        return self.y_pos

    def on_hit(self):
        # print('coin graphic hit')
        self.just_hit = True
        self.hit = True

    def on_pass(self):
        # print('coin graphic pass')
        self.passed = True
        self.color.rgb = (0.25, 0.25, 0.25)
        self.shadow_color.a = 0.5

    def on_update(self, now_time):
        # update the coin's points given the current time
        self.y_pos = time_to_ypos(self.time - now_time)
        self.radius = abs((Window.height - self.y_pos) / Window.height * (self.max_size - self.initial_size) + self.initial_size)

        self.cbpos = map_coords_3D_to_2D(self.x_pos, self.y_pos, 0)
        self.csize = (self.radius, self.radius)

        if self.just_hit:
            self.size_ratio_anim = KFAnim((now_time, 1.0), (now_time + 0.2, 2))
            self.alpha_anim = KFAnim((now_time, 1.0), (now_time + 0.2, 0))
            self.just_hit = False

        if self.hit:
            size_ratio = self.size_ratio_anim.eval(now_time)
            alpha = self.alpha_anim.eval(now_time)
            self.csize = (self.radius * size_ratio, self.radius * size_ratio)
            self.color.a = alpha
            self.shadow_color.a = alpha / 4.0

        self.coin.cbpos = self.cbpos
        self.coin.csize = self.csize

        self.shadow.cbpos = (self.cbpos[0], self.cbpos[1] - self.radius * shadow_ypos_radius_multiplier)
        self.shadow.csize = (self.csize[0] * shadow_x_size_multiplier, self.csize[1] * shadow_y_size_multiplier)

        # make coin visible/not visible depending on y position
        if - self.radius <= self.y_pos < Window.height:
            if self.coin not in self.children:
                self.add(self.color)
                self.add(self.coin)
                self.add(self.shadow_color)
                self.add(self.shadow)
        else:
            if self.coin in self.children:
                self.remove(self.color)
                self.remove(self.coin)
                self.remove(self.shadow_color)
                self.remove(self.shadow)

    def on_resize(self, win_size):
        self.x_pos = self.tracks.get_lane_center_x(self.lane)               # start in middle of lane
        self.y_pos = Window.height                                          # start at top of screen
        self.initial_size = Window.height * initial_size_multiplier
        self.max_size = Window.height * max_size_multiplier
        self.radius = abs((Window.height - self.y_pos) / Window.height * (self.max_size - self.initial_size) + self.initial_size)
        
        # the x,y coordinates on the screen
        self.cbpos = map_coords_3D_to_2D(self.x_pos, self.y_pos, 0)
        self.csize = (self.radius, self.radius)

        # the coin drawing - a CEllipse
        self.coin.cbpos = self.cbpos
        self.coin.cbsize = self.csize
        
        self.shadow.cbpos = (self.cbpos[0], self.cbpos[1] - self.radius * shadow_ypos_radius_multiplier)
        self.shadow.csize = (self.csize[0] * shadow_x_size_multiplier, self.csize[1] * shadow_y_size_multiplier)



class InstrumentIcon(InstructionGroup):

    # icon that shows what instrument is being played during regular mode
    
    def __init__(self):

        super(InstrumentIcon, self).__init__()

        self.pos = (Window.width*0.5, Window.height*0.86)
        # self.text_pos = (Window.width*0.5, Window.height*0.7)
        self.size = (Window.width*0.13, Window.width*0.13)
        self.instrument = "violin"
        self.token = CRectangle(cpos=self.pos, csize=self.size, texture=Image(instrument_paths[self.instrument]).texture)
        # self.text = CLabelRect(cpos=self.pos, text=f"instrument: {self.instrument}")
        self.color = Color(1, 1, 1)

        self.add(self.color)
        self.add(self.token)
        # self.add(Color(0, 0, 0))
        # self.add(self.text)

        self.hit_anim = KFAnim((0, Window.width*0.13*1.3), (0.1, Window.width*0.13))

        self.anim_on = False
        self.hit_time = 0
        self.time = 0

    def change_instrument(self, new_instrument):

        self.instrument = new_instrument
        self.token.texture = Image(instrument_paths[new_instrument]).texture

    def on_hit(self):
        self.color.rgb = (1, 1, 1)
        self.hit_time = self.time
        self.anim_on = True
        
    def on_pass(self):
        self.color.rgb = (0.25, 0.25, 0.25)
    
    def on_update(self, now):
        
        self.time = now
        
        if self.anim_on:
            time_since_hit = now - self.hit_time
            if time_since_hit < 0.1:
                new_size = self.hit_anim.eval(time_since_hit)
                self.token.set_csize((new_size, new_size))
            else:
                self.anim_on = False
    
    def on_resize(self, win_size):

        self.pos = (win_size[0]*0.5, win_size[1]*0.86)
        self.size = (win_size[0]*0.13, win_size[0]*0.13)
        # self.text_pos = (win_size[0]*0.8, win_size[1]*0.75)
        self.token.set_cpos(self.pos)
        self.token.set_csize(self.size)
        # self.text.set_cpos(self.text_pos)