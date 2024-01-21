from imslib.gfxutil import topleft_label, CEllipse, KFAnim, AnimGroup, CRectangle

from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Rectangle, Line, Quad
from kivy.graphics import PushMatrix, PopMatrix, Translate, Scale, Rotate
from kivy.core.image import Image

from kivy.core.window import Window

from helper_funcs import *

height_to_width_ratio = 1.3

class Train(InstructionGroup):
    
    def __init__(self, tracks, lane, start_time, end_time):
        super(Train, self).__init__()

        assert start_time < end_time, "start_time should be before end_time for train"

        self.tracks = tracks
        self.lane = lane
        self.start_time = start_time + 0.15
        self.end_time = end_time - 0.15

        self.left_x, self.right_x = self.tracks.get_lane_track_borders_x(self.lane)
        self.y_start = time_to_ypos(self.start_time - 0)
        self.y_end = time_to_ypos(self.end_time - 0)
        self.z = 0
        self.dz = 0

        self.true_width = self.right_x - self.left_x
        self.true_height = self.true_width * height_to_width_ratio * get_effective_width_ratio()

        self.shadow_color = Color(0.5, 0.5, 0.5)
        self.shadow_color.a = 0.25
        self.shadow = Quad(points=(0,0,0,0,0,0,0,0))

        self.color = Color(1,1,1)
        self.left = Quad(points=(0,0,0,0,0,0,0,0),texture=Image('./data/images/trains/side.png').texture)
        self.right = Quad(points=(0,0,0,0,0,0,0,0),texture=Image('./data/images/trains/side.png').texture)
        self.top = Quad(points=(0,0,0,0,0,0,0,0),texture=Image('./data/images/trains/top.png').texture)
        self.front = Quad(points=(0,0,0,0,0,0,0,0),texture=Image('./data/images/trains/front.png').texture)

        self.all_objs = (self.shadow_color, self.shadow, self.color, self.left, self.right, self.top, self.front)

        self.update_train()
    

    def get_train_y_pos(self):
        # Returns (y pos of front of train, y pos of back of train)
        return self.left.points[1], self.left.points[5]


    def switch_mode(self, on_screen):
        if on_screen:
            if self.z == 0:
                self.dz = -dz
            # elif self.z >= -Window.height * post_height_ratio:
            else:
                self.dz = dz
        else:
            self.dz = 0
            if self.z == 0:
                self.z = -Window.height * post_height_ratio
            else:
                self.z = 0

        self.color.a = get_new_mode_alpha(self.color)


    def on_update(self, now_time):
        if self.dz < 0 and self.z > -Window.height * post_height_ratio:
            self.z = max(self.z + self.dz, -Window.height * post_height_ratio)
        elif self.dz > 0 and self.z < 0:
            self.z = min(self.z + self.dz, 0)
        else:
            self.dz = 0

        self.y_start = time_to_ypos(self.start_time - now_time)
        self.y_end = time_to_ypos(self.end_time - now_time)

        self.update_train()


    def on_resize(self, win_size):
        self.y_start = time_to_ypos(self.start_time - 0)
        self.y_end = time_to_ypos(self.end_time - 0)

        self.left_x, self.right_x = self.tracks.get_lane_track_borders_x(self.lane)
        self.true_width = self.right_x - self.left_x
        self.true_height = self.true_width * height_to_width_ratio * get_effective_width_ratio()

        self.update_train()


    def update_train(self):
        if self.y_start < Window.height:
            if self.y_end > Window.height:
                self.y_end = Window.height

            # s/e = start/end
            # b/t = bottom/top
            # l/r = left/right

            x_sbl, y_sbl = map_coords_3D_to_2D(self.left_x, self.y_start, self.z)
            x_sbr, y_sbr = map_coords_3D_to_2D(self.right_x, self.y_start, self.z)
            x_ebl, y_ebl = map_coords_3D_to_2D(self.left_x, self.y_end, self.z)
            x_ebr, y_ebr = map_coords_3D_to_2D(self.right_x, self.y_end, self.z)

            x_stl, y_stl = map_coords_3D_to_2D(self.left_x, self.y_start, self.z + self.true_height)
            x_str, y_str = map_coords_3D_to_2D(self.right_x, self.y_start, self.z + self.true_height)
            x_etl, y_etl = map_coords_3D_to_2D(self.left_x, self.y_end, self.z + self.true_height)
            x_etr, y_etr = map_coords_3D_to_2D(self.right_x, self.y_end, self.z + self.true_height)
            

            self.shadow.points = (x_sbl, y_sbl, x_sbr, y_sbr, x_ebl, y_ebl, x_ebr, y_ebr)
            self.left.points = (x_sbl, y_sbl, x_ebl, y_ebl, x_etl, y_etl, x_stl, y_stl)
            self.right.points = (x_sbr, y_sbr, x_ebr, y_ebr, x_etr, y_etr, x_str, y_str)
            self.top.points = (x_str, y_str, x_etr, y_etr, x_etl, y_etl, x_stl, y_stl)
            self.front.points = (x_sbl, y_sbl, x_sbr, y_sbr, x_str, y_str, x_stl, y_stl)

            if self.y_start >= Window.height or y_etl <= 0:
                for obj in self.all_objs:
                    if obj in self.children:
                        self.remove(obj)
            else:
                for obj in self.all_objs:
                    if obj not in self.children:
                        self.add(obj)