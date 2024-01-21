from imslib.gfxutil import topleft_label, CEllipse, KFAnim, AnimGroup, CRectangle

from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Rectangle, Line, Quad
from kivy.graphics import PushMatrix, PopMatrix, Translate, Scale, Rotate
from kivy.core.image import Image

from kivy.core.window import Window

import numpy as np

from helper_funcs import *

gravity = np.array((0, -1800))
x_vel_multiplier = 1 / 1.5 # 1/c where the smaller c is, the faster the player switches lanes

class PlayerGraphics(InstructionGroup):
    
    def __init__(self, tracks):
        super(PlayerGraphics, self).__init__()

        self.tracks = tracks

        self.lane = 1               # 0-indexed lanes!
        self.next_lane = 1
        self.in_lane_status = [False, True, False]
        self.velocity = [0,0]       # velocity of the player in xy, used for jumping / switching lanes
        self.right_front = True     # variable indicating that the right leg is in front
        self.is_jumping = False     # is jumping
        self.is_running = False     # is running

        self.body_dim = (Window.height/16, Window.height/8) # 35, 40
        self.leg_w = self.body_dim[0]/2         # 12
        self.long_leg_h = self.body_dim[1]/2    # 30
        self.short_leg_h = self.body_dim[1]/4   # 15

        self.leg_speed = Window.height / 15     # 50
        # self.x_velocity = Window.width / 4      # 200... moving up to 250
        self.x_velocity = Window.width * x_vel_multiplier

        self.body_x_pos, self.nowbar_y = self.tracks.get_player_pos(self.lane)
        self.body_y_pos = self.nowbar_y + self.long_leg_h + self.body_dim[1]

        # all the body parts, stored in self.objects for simplicity
        self.body = CTRectangle(ctpos=(self.body_x_pos, self.body_y_pos), ctsize = self.body_dim, texture=Image('./data/images/nutcracker/nutcracker_body.png').texture)
        self.left_leg = CTRectangle(ctpos=(self.body_x_pos - self.leg_w/2, self.body_y_pos - self.body_dim[1]), ctsize=(self.leg_w, self.long_leg_h), texture=Image('./data/images/nutcracker/nutcracker_left_leg.png').texture)
        self.right_leg = CTRectangle(ctpos=(self.body_x_pos + self.leg_w/2, self.body_y_pos - self.body_dim[1]), ctsize=(self.leg_w, self.short_leg_h), texture=Image('./data/images/nutcracker/nutcracker_right_leg.png').texture)
        
        # shadow
        self.shadow_color = Color(0, 0, 0)
        self.shadow_color.a = 0.25
        self.shadow = CEllipse(cpos = (0,0), csize = (self.body_dim[0]*1.5, self.body_dim[0]*0.5))
        self.objects = (self.body, self.left_leg, self.right_leg, self.shadow_color, self.shadow)

        self.add(Color(1,1,1))

        for obj in self.objects:
            self.add(obj)

    def get_foot_y_pos(self):
        return min(self.left_leg.ctpos[1] - self.left_leg.ctsize[1], self.right_leg.ctpos[1] - self.right_leg.ctsize[1])
    
    def is_on_ground(self):
        return not self.is_jumping
    
    def get_lane(self):
        if True not in self.in_lane_status:
            return None
        else:
            return self.in_lane_status.index(True)
        
    def on_train_side_collision(self):
        self.velocity[0] = -1 * self.velocity[0]
        self.lane, self.next_lane = self.next_lane, self.lane
        self.body_x_pos, self.nowbar_y = self.tracks.get_player_pos(self.next_lane)
        self.body_y_pos = self.nowbar_y + self.long_leg_h + self.body_dim[1]
        self.update_pos(0.1)

    def switch_lanes(self, direction):
        # direction = True for right, False for left
        # updates the velocity and lane
        if direction and self.next_lane != 2:
            self.next_lane += 1
            self.velocity[0] = self.x_velocity
        elif not direction and self.next_lane != 0:
            self.next_lane -= 1
            self.velocity[0] = -1 * self.x_velocity
        self.body_x_pos, self.nowbar_y = self.tracks.get_player_pos(self.next_lane)
        self.body_y_pos = self.nowbar_y + self.long_leg_h + self.body_dim[1]

    def start_running(self):
        self.is_running = True
    
    def stop_running(self):
        self.is_running = False

    def jump(self):
        # called by the mainWidget when jumping
        if not self.is_jumping:
            self.velocity[1] = Window.height * 0.71
            self.is_jumping = True

    def on_game_over(self):
        self.stop_running()

    def update_legs(self, dt):
        # updates the leg dimensions to imitate running
        if self.is_running:
            right_h = self.right_leg.get_ctsize()[1]
            left_h = self.left_leg.get_ctsize()[1]
            dlength = self.leg_speed*dt

            if dlength < self.short_leg_h: # this if statement considers the beginning when dt is massive
                if self.right_front:    
                    self.right_leg.set_ctsize((self.leg_w, right_h + dlength))
                    self.left_leg.set_ctsize((self.leg_w, left_h - dlength))
                    if left_h - dlength <= self.short_leg_h:
                        self.right_front = False
                else:
                    self.right_leg.set_ctsize((self.leg_w, right_h - dlength))
                    self.left_leg.set_ctsize((self.leg_w, left_h + dlength))
                    if right_h - dlength <= self.short_leg_h:
                        self.right_front = True

    def update_jump(self, dt):
        # updates the y-velocity when in a jump
        if self.is_jumping:
            self.velocity[1] = self.velocity[1] + gravity[1] * dt
            if self.body.get_ctpos()[1] <= self.body_y_pos and self.velocity[1] < 0:
                self.is_jumping = False
                self.velocity[1] = 0

    def update_switch_lanes(self, dt):
        # stops the x movement once the player has reached the new lane
        left, right = self.tracks.get_mapped_lane_track_borders_at_nowbar(self.lane)
        next_left, next_right = self.tracks.get_mapped_lane_track_borders_at_nowbar(self.next_lane)
        if self.velocity[0] > 0:
            if self.body.get_ctpos()[0] >= self.body_x_pos - 30:
                self.velocity[0] = 0
                self.lane = self.next_lane
            elif self.body.get_ctpos()[0] >= next_left - 30:
                self.in_lane_status[self.next_lane] = True
                # self.lane = self.next_lane
            elif self.body.get_ctpos()[0] >= right - 30:
                self.in_lane_status[self.lane] = False
                
        if self.velocity[0] < 0:
            if self.body.get_ctpos()[0] <= self.body_x_pos + 30:
                self.velocity[0] = 0
                self.lane = self.next_lane
            elif self.body.get_ctpos()[0] <= next_right + 30:
                self.in_lane_status[self.next_lane] = True
                # self.lane = self.next_lane
            elif self.body.get_ctpos()[0] <= left + 30:
                self.in_lane_status[self.lane] = False

        
    def update_pos(self, dt):
        # updates all the body parts' positions
        pos = self.body.get_ctpos()
        x = pos[0] + dt * self.velocity[0]
        # if self.velocity[0] > 0:
        #     x = min(x, self.body_x_pos)
        # elif self.velocity[0] < 0:
        #     x = max(x, self.body_x_pos)
        if self.velocity[0] == 0:
            x = self.body_x_pos
        y = max(pos[1] + dt * self.velocity[1], self.body_y_pos)
        self.body.set_ctpos((x, y))
        self.left_leg.set_ctpos((x - self.leg_w/2, y - self.body_dim[1]))
        self.right_leg.set_ctpos((x + self.leg_w/2, y - self.body_dim[1]))
        self.shadow.set_cpos((x, self.nowbar_y))

    def on_resize(self, win_size):
        width, height = win_size

        self.body_dim = (height/16, height/8) # 35, 40
        self.leg_w = self.body_dim[0]/2         # 12
        self.long_leg_h = self.body_dim[1]/2    # 30
        self.short_leg_h = self.body_dim[1]/4   # 15

        self.leg_speed = height / 15     # 50
        # self.x_velocity = width / 4      # 200... moving up to 250
        self.x_velocity = Window.width * x_vel_multiplier
        
        self.body_x_pos, self.nowbar_y = self.tracks.get_player_pos(self.lane)
        self.body_y_pos = self.nowbar_y + self.long_leg_h + self.body_dim[1]

        self.body.ctpos = (self.body_x_pos, self.body_y_pos)
        self.body.ctsize = self.body_dim
        self.left_leg.ctpos = (self.body_x_pos - self.leg_w/2, self.body_y_pos - self.body_dim[1])
        self.left_leg.ctsize = (self.leg_w, self.long_leg_h)
        self.right_leg.ctpos=(self.body_x_pos + self.leg_w/2, self.body_y_pos - self.body_dim[1])
        self.right_leg.ctsize=(self.leg_w, self.short_leg_h)

    def on_update(self, dt):
        self.update_legs(dt)
        self.update_jump(dt)
        self.update_switch_lanes(dt)
        self.update_pos(dt)
