import random
from helper_funcs import *

from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Rectangle, Line, Quad
from imslib.gfxutil import topleft_label, CEllipse, KFAnim, AnimGroup, CRectangle
from kivy.core.image import Image

# height_to_width_ratio = 0.2
# initial_size = 10
# max_size = 40

height_to_width_ratio = 0.2
initial_size_multiplier = 1/70
max_size_multiplier = 1/15
shadow_ypos_radius_multiplier = 0.4
shadow_x_size_multiplier = 1.25
shadow_y_size_multiplier = 0.5

class ImprovToken(InstructionGroup):

    def __init__(self, tracks, lane, time):

        super(ImprovToken, self).__init__()

        # coin variables
        self.tracks = tracks
        self.lane = lane
        self.time = time # should be when a new section starts in the song

        # location/dimensions of the coin
        self.x_pos = self.tracks.get_lane_center_x(self.lane)               # start in middle of lane
        self.y_pos = Window.height                                          # start at top of screen
        self.initial_size = Window.height * initial_size_multiplier
        self.max_size = Window.height * max_size_multiplier
        self.radius = abs((Window.height - self.y_pos) / Window.height * (self.max_size - self.initial_size) + self.initial_size)

        # x,y coordinates on the screen
        self.cbpos = map_coords_3D_to_2D(self.x_pos, self.y_pos, 0)
        self.csize = (self.radius, self.radius)

        # token drawing
        # TODO: add texture image to token (of the instrument that is to be played)
        self.token = CBEllipse(cbpos=self.cbpos, cbsize = self.csize, texture=Image('./data/images/tokens/tambourine.png').texture)
        self.shadow = CBEllipse(cbpos=(self.cbpos[0], self.cbpos[1] - self.radius * shadow_ypos_radius_multiplier), cbsize=(self.csize[0] * shadow_x_size_multiplier, self.csize[1] * shadow_y_size_multiplier))

        self.color = Color(1, 1, 0)
        self.add(self.color)
        self.add(self.token)

        self.shadow_color = Color(0, 0, 0)
        self.shadow_color.a = 0.25
        self.add(self.shadow_color)
        self.add(self.shadow)

        self.collected = False
    
    def get_lane(self):
        return self.lane
    def get_time(self):
        return self.time

    def on_collect(self):
        # print('improv token collected')
        self.color.a = 0
        self.remove(self.token)
    
    def on_pass(self):
        self.remove(self.token)
        self.remove(self.color)
        self.color = Color(0.5, 0.5, 0.5)
        self.add(self.color)
        self.add(self.token)
    
    def on_update(self, now_time):
        # update the coin's points given the current time
        self.y_pos = time_to_ypos(self.time - now_time)
        self.radius = abs((Window.height - self.y_pos) / Window.height * (self.max_size - self.initial_size) + self.initial_size)

        self.cbpos = map_coords_3D_to_2D(self.x_pos, self.y_pos, 0)
        self.csize = (self.radius, self.radius)

        self.token.cbpos = self.cbpos
        self.token.cbsize = self.csize

        self.shadow.cbpos = (self.cbpos[0], self.cbpos[1] - self.radius * shadow_ypos_radius_multiplier)
        self.shadow.csize = (self.csize[0] * shadow_x_size_multiplier, self.csize[1] * shadow_y_size_multiplier)

        # make coin visible/not visible depending on y position
        if self.y_pos < Window.height:
            if self.token not in self.children:
                self.add(self.color)
                self.add(self.token)
                self.add(self.shadow_color)
                self.add(self.shadow)
        else:
            if self.token in self.children:
                self.remove(self.color)
                self.remove(self.token)
                self.remove(self.shadow_color)
                self.remove(self.shadow)

    def on_resize(self, win_size):
        self.x_pos = self.tracks.get_lane_center_x(self.lane)               # start in middle of lane
        self.y_pos = win_size[1]                                      # start at top of screen
        self.initial_size = win_size[1]  * initial_size_multiplier
        self.max_size = win_size[1]  * max_size_multiplier
        self.radius = abs((win_size[1]  - self.y_pos) / win_size[1]  * (self.max_size - self.initial_size) + self.initial_size)
        
        # the x,y coordinates on the screen
        self.cbpos = map_coords_3D_to_2D(self.x_pos, self.y_pos, 0)
        self.csize = (self.radius, self.radius)

        # the coin drawing - a CEllipse
        self.token.cbpos = self.cbpos
        self.token.cbsize = self.csize
        
        self.shadow.cbpos = (self.cbpos[0], self.cbpos[1] - self.radius * shadow_ypos_radius_multiplier)
        self.shadow.csize = (self.csize[0] * shadow_x_size_multiplier, self.csize[1] * shadow_y_size_multiplier)

class ImprovIcon(InstructionGroup):

    # icon that pops up during improv mode
    # displays: instrument that can be played right now
    #           feedback on press
    def __init__(self):

        super(ImprovIcon, self).__init__()
        
        self.pos = (Window.width*0.5, Window.height*0.8)
        self.size = (Window.width*0.13, Window.width*0.13)
        self.token = CRectangle(cpos=self.pos, csize=self.size, texture=Image('./data/images/tokens/tambourine_gold.png').texture)
        self.color = Color(1, 1, 1)

        self.add(self.color)
        self.add(self.token)
        
        self.hit_anim = KFAnim((0, Window.width*0.13*1.3), (0.1, Window.width*0.13))

        self.anim_on = False
        self.hit_time = 0
        self.time = 0
    
    def on_hit(self):

        self.hit_time = self.time
        self.anim_on = True
        
    
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

        self.token.set_csize((win_size[0]*0.13, win_size[0]*0.13))
        self.token.set_cpos((win_size[0]*0.5, win_size[1]*0.8))
        self.hit_anim = KFAnim((0, win_size[0]*0.13*1.3), (0.1, win_size[0]*0.13))