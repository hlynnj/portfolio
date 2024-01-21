from imslib.gfxutil import topleft_label, CEllipse, KFAnim, AnimGroup, CRectangle
from kivy.core.image import Image

from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Rectangle, Line, Quad
from kivy.graphics import PushMatrix, PopMatrix, Translate, Scale, Rotate

from kivy.core.window import Window

from helper_funcs import *

height_to_width_ratio = 0.75

class Obstacle(InstructionGroup):
    
    def __init__(self, tracks, lane, time):
        super(Obstacle, self).__init__()

        # obstacle variables
        self.tracks = tracks
        self.lane = lane
        self.time = time + 0.15          # time in the song that the obstacle should be in the nowbar

        # dimensions of the obstacle
        self.left_x, self.right_x = self.tracks.get_lane_track_borders_x(self.lane)     # left and right x-coord of obstacle
        self.y_pos = time_to_ypos(self.time - 0)                              # starts at the top of the screen
        self.z = 0
        self.dz = 0

        self.true_width = self.right_x - self.left_x
        self.true_height = self.true_width * height_to_width_ratio * get_effective_width_ratio()

        # the obstacle drawing - a quad and two line posts
        self.color = Color(1,1,1)
        self.quad = Quad(points=(0,0,0,0,0,0,0,0), texture=Image('./data/images/tracks/barricade.png').texture)
        self.leg_color = Color(1, 0, 0)
        self.left_post = Line(points=(0,0,0,0), width=2)
        self.right_post = Line(points=(0,0,0,0), width=2)

        # shadow
        self.shadow_color = Color(0, 0, 0)
        self.shadow_color.a = 0.25
        self.shadow = Quad(points=(0,0,0,0,0,0,0,0))

        self.all_objs = (self.color, self.quad, self.leg_color, self.left_post, self.right_post, self.shadow_color, self.shadow)

        self.update_obstacle()

    
    def get_perceived_height(self):
        # used for player collision detection
        return self.left_post.points[1]
    
    
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
        self.leg_color.a = get_new_mode_alpha(self.leg_color)

    def on_update(self, now_time):
        # update the obstacle's points given the current time
        if self.dz < 0 and self.z > -Window.height * post_height_ratio:
            self.z = max(self.z + self.dz, -Window.height * post_height_ratio)
        elif self.dz > 0 and self.z < 0:
            self.z = min(self.z + self.dz, 0)
        else:
            self.dz = 0

        # print(self.z)
        self.y_pos = time_to_ypos(self.time - now_time)
        self.update_obstacle()


    def on_resize(self, win_size):
        self.left_x, self.right_x = self.tracks.get_lane_track_borders_x(self.lane)
        self.true_width = self.right_x - self.left_x
        self.true_height = self.true_width * height_to_width_ratio * get_effective_width_ratio()
        self.y_pos = time_to_ypos(self.time - 0)
        self.update_obstacle()


    def update_obstacle(self):
        if self.y_pos < Window.height:
            # Get xy coordinates
            x5, y5 = map_coords_3D_to_2D(self.left_x, self.y_pos, self.z)
            x6, y6 = map_coords_3D_to_2D(self.right_x, self.y_pos, self.z)

            x1, y1 = map_coords_3D_to_2D(self.left_x, self.y_pos, self.z + self.true_height/4)       # bottom left of quad
            x2, y2 = map_coords_3D_to_2D(self.right_x, self.y_pos, self.z + self.true_height/4)       # bottom right of quad
            x3, y3 = map_coords_3D_to_2D(self.right_x, self.y_pos, self.z + self.true_height)         # top right of quad
            x4, y4 = map_coords_3D_to_2D(self.left_x, self.y_pos, self.z + self.true_height)         # top left of quad

            self.quad.points = (x1, y1, x2, y2, x3, y3, x4, y4)
            self.left_post.points = (x4, y4, x5, y5)
            self.right_post.points = (x3, y3, x6, y6)

            # adjust shadow coordinates
            # x5, y5 is bottom left, x6, y6 is bottom right
            top_left_x, top_left_y = map_coords_3D_to_2D(self.left_x, self.y_pos + (self.true_height * 0.07), self.z)
            bottom_left_x, bottom_left_y = map_coords_3D_to_2D(self.left_x, self.y_pos - (self.true_height * 0.07), self.z)
            top_right_x, top_right_y = map_coords_3D_to_2D(self.right_x, self.y_pos + (self.true_height * 0.07), self.z)
            bottom_right_x, bottom_right_y = map_coords_3D_to_2D(self.right_x, self.y_pos - (self.true_height * 0.07), self.z)

            self.shadow.points = (bottom_left_x, bottom_left_y, bottom_right_x, bottom_right_y, top_right_x, top_right_y, top_left_x, top_left_y)

            if self.y_pos >= Window.height or y3 <= 0:
                for obj in self.all_objs:
                    if obj in self.children:
                        self.remove(obj)
            else:
                for obj in self.all_objs:
                    if obj not in self.children:
                        self.add(obj)
