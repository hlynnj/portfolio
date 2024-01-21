from imslib.gfxutil import topleft_label, CEllipse, KFAnim, AnimGroup, CRectangle
from kivy.core.image import Image

from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Rectangle, Line, Quad
from kivy.graphics import PushMatrix, PopMatrix, Translate, Scale, Rotate

from kivy.core.window import Window

from helper_funcs import *
import numpy as np

class TracksGraphics(InstructionGroup):
    # all the lines have points in the form [x1, y1, x2, y2], where (x1, y1) are the endpoints at y=0 and (x2, y2) are the endpoints at horizon    
    def __init__(self):
        super(TracksGraphics, self).__init__()

        w = Window.width
        h = Window.height

        self.lane_width = Window.width / 4
        self.track_width = self.lane_width / 2
        self.rung_width = self.track_width * 4 / 3
        self.wire_width = self.track_width * 2 / 3

        self.z = 0
        self.dz = 0
        self.horizon_y = map_coords_3D_to_2D(0, h, self.z)[1]
        self.nowbar_y = h * nowbar_y

        self.lane_borders_x = []
        for i in range(4):
            self.lane_borders_x.append(w/2 + (2*i-3)/2*self.lane_width)

        # ground

        # self.add(Color(0.87, 0.72, 0.53))
        self.add(Color(1, 1, 1))
        self.background = Rectangle(pos=(0,0),size=(w,h)) # snowy vibes
        # self.background = Rectangle(pos=(0,0), size=(w,h), texture=Image('./data/images/tracks/snow_background.jpg').texture)
    
        self.add(self.background)

        # train tracks

        self.rung_borders_x = []
        self.wire_x = []
        self.track_lines = []
        self.track_color = Color(0.5, 0.5, 0.5)
        self.add(self.track_color) # track color
        # self.add(Color(0, 0, 0))
        for i in range(3):
            center_x = self.get_lane_center_x(i)
            left = Line(points=[*map_coords_3D_to_2D(center_x - self.track_width/2, h, self.z), *map_coords_3D_to_2D(center_x - self.track_width/2, 0, self.z)], width=3)
            right = Line(points=[*map_coords_3D_to_2D(center_x + self.track_width/2, h, self.z), *map_coords_3D_to_2D(center_x + self.track_width/2, 0, self.z)], width=3)
            self.track_lines.append((left, right))
            self.add(left)
            self.add(right)

            self.rung_borders_x.append((center_x - self.rung_width/2, center_x + self.rung_width/2))
            self.wire_x += [center_x - self.wire_width/2, center_x + self.wire_width/2]

        self.rungs = [[], [], []]
        self.num_rungs_per_lane = 10
        for i in range(3):
            for j in range(self.num_rungs_per_lane):
                rung = TrackRung(Window.height * (j+1) / self.num_rungs_per_lane , self.rung_borders_x[i])
                self.rungs[i].append(rung)
                self.add(rung)

        self.add(Color(0.53,0.81,0.95))
        self.horizon = Rectangle(pos = (0,self.horizon_y), size = (Window.width, Window.height - self.horizon_y))
        self.add(self.horizon)

        self.posts = []
        self.num_posts_per_screen = 4
        for i in range(self.num_posts_per_screen):
            self.posts.append(ElectricityPost(2 * Window.height * (i) / self.num_posts_per_screen, 2 * Window.height * (i+1) / self.num_posts_per_screen, (self.rung_borders_x[0][0], self.rung_borders_x[2][1]), self.wire_x))
            # self.add(self.posts[-1])

    def get_player_pos(self, lane):
        '''
        lane - either 0, 1, 2, indicating which lane the player is in
        
        returns (x,y) position of where the player's torso center should be
        '''
        
        return map_coords_3D_to_2D(self.get_lane_center_x(lane), self.nowbar_y, 0)
    
    def get_lane_center_x(self, lane):
        '''
        lane - either 0, 1, 2, indicating which lane to get

        returns x value of the line at the center of the lane
        '''
        return (self.lane_borders_x[lane] + self.lane_borders_x[lane+1])/2
    
    def get_lane_track_borders_x(self, lane):
        '''
        lane - either 0, 1, 2, indicating which lane to get

        returns x value of the left and right track borders on that lane
        '''
        return (self.get_lane_center_x(lane) - self.track_width/2, self.get_lane_center_x(lane) + self.track_width/2)

    def get_mapped_lane_track_borders_at_nowbar(self, lane):
        return (map_coords_3D_to_2D(self.get_lane_track_borders_x(lane)[0], self.nowbar_y, self.z)[0], map_coords_3D_to_2D(self.get_lane_track_borders_x(lane)[1], self.nowbar_y, self.z)[0])

    def start_anim(self):
        # starts the animation for all the rungs
        for i in range(3):
            for rung in self.rungs[i]:
                rung.start_anim()

        for post in self.posts:
            post.start_anim()

    def stop_anim(self):
        # starts the animation for all the rungs
        for i in range(3):
            for rung in self.rungs[i]:
                rung.stop_anim()

        for post in self.posts:
            post.stop_anim()

    def switch_mode(self):
        if self.z == 0:
            self.dz = -dz
        elif self.z >= -Window.height * post_height_ratio:
            self.dz = dz

        for i in range(3):
            for rung in self.rungs[i]:
                rung.switch_mode()

        for post in self.posts:
            post.switch_mode()

        self.track_color.a = get_new_mode_alpha(self.track_color)

    def update_lines(self):
        for i in range(4):
            self.lane_borders_x[i] = Window.width/2 + (2*i-3)/2*self.lane_width
        
        self.horizon_y = map_coords_3D_to_2D(0, Window.height, self.z)[1]
        self.nowbar_y = Window.height * nowbar_y

        for i in range(3):
            center_x = self.get_lane_center_x(i)
            self.track_lines[i][0].points=[*map_coords_3D_to_2D(center_x - self.track_width/2, Window.height, self.z), *map_coords_3D_to_2D(center_x - self.track_width/2, 0, self.z)]
            self.track_lines[i][1].points=[*map_coords_3D_to_2D(center_x + self.track_width/2, Window.height, self.z), *map_coords_3D_to_2D(center_x + self.track_width/2, 0, self.z)]

            self.rung_borders_x[i] = (center_x - self.rung_width/2, center_x + self.rung_width/2)
            self.wire_x[2*i:2*i+2] = [center_x - self.wire_width/2, center_x + self.wire_width/2]

        self.background.size = (Window.width, Window.height)
        self.horizon.pos = (0,self.horizon_y)
        self.horizon.size = (Window.width, Window.height - self.horizon_y)

    def on_update(self, dt):
        # updates all the rungs
        if self.dz < 0 and self.z > -Window.height * post_height_ratio:
            self.z = max(self.z + self.dz, -Window.height * post_height_ratio)
            self.update_lines()
        elif self.dz > 0 and self.z < 0:
            self.z = min(self.z + self.dz, 0)
            self.update_lines()
        else:
            self.dz = 0

        for i in range(3):
            for rung in self.rungs[i]:
                rung.on_update(dt)

        for post in self.posts:
            post.on_update(dt)

    def on_resize(self, win_size):
        width, height = win_size

        self.lane_width = width / 4
        self.track_width = self.lane_width / 2
        self.rung_width = self.track_width * 4 / 3
        self.wire_width = self.track_width * 2 / 3

        self.update_lines()

        for i in range(3):
            for j in range(self.num_rungs_per_lane):
                self.rungs[i][j].on_resize(win_size, height * (j+1) / self.num_rungs_per_lane, self.rung_borders_x[i])

        for i in range(self.num_posts_per_screen):
            self.posts[i].on_resize(win_size, 2 * height * (i) / self.num_posts_per_screen, 2 * height * (i+1) / self.num_posts_per_screen, (self.rung_borders_x[0][0], self.rung_borders_x[2][1]))
            
    def get_posts(self):
        return self.posts
        
rung_height_to_width_ratio = 0.1

class TrackRung(InstructionGroup):
    
    def __init__(self, start_y, border_lines):
        super(TrackRung, self).__init__()

        self.left_border_x = border_lines[0]
        self.right_border_x = border_lines[1]

        self.w = self.right_border_x - self.left_border_x
        self.h = rung_height_to_width_ratio * self.w

        self.z = 0
        self.dz = 0

        x1, y1 = map_coords_3D_to_2D(self.left_border_x, start_y, self.z)   # top left
        x2, y2 = map_coords_3D_to_2D(self.right_border_x, start_y, self.z)   # top right
        x3, y3 = map_coords_3D_to_2D(self.right_border_x, start_y - self.h, self.z)   # bottom right
        x4, y4 = map_coords_3D_to_2D(self.left_border_x, start_y - self.h, self.z)   # bottom left

        self.color = Color(1,1,1)
        self.rung = Quad(points = (x1, y1, x2, y2, x3, y3, x4, y4), texture=Image('./data/images/tracks/wooden_plank.png').texture)
        self.add(self.color)
        self.add(self.rung)

        self.time = 0
        self.anim = False

        first_time_span = time_span * start_y / Window.height
        self.pos_anim = KFAnim((self.time, start_y), (self.time+first_time_span, 0))

    def start_anim(self):
        self.anim = True

    def stop_anim(self):
        self.anim = False

    def switch_mode(self):
        if self.z == 0:
            self.dz = -dz
        elif self.z >= -Window.height * post_height_ratio:
            self.dz = dz
        self.color.a = get_new_mode_alpha(self.color)

    def update_points(self, y):
        if y <= 0:
            y = Window.height
            self.pos_anim = KFAnim((self.time, Window.height), (self.time+time_span, 0))

        x1, y1 = map_coords_3D_to_2D(self.left_border_x, y, self.z)
        x2, y2 = map_coords_3D_to_2D(self.right_border_x, y, self.z)   # top right
        x3, y3 = map_coords_3D_to_2D(self.right_border_x, y - self.h, self.z)   # bottom right
        x4, y4 = map_coords_3D_to_2D(self.left_border_x, y - self.h, self.z)   # bottom left

        self.rung.points = (x1, y1, x2, y2, x3, y3, x4, y4)

    def on_update(self, dt):
        if self.dz < 0 and self.z > -Window.height * post_height_ratio:
            self.z = max(self.z + self.dz, -Window.height * post_height_ratio)
        elif self.dz > 0 and self.z < 0:
            self.z = min(self.z + self.dz, 0)
        else:
            self.dz = 0

        if self.anim:
            y = self.pos_anim.eval(self.time)
            self.update_points(y)
            self.time += dt

    def on_resize(self, win_size, start_y, border_lines):
        width, height = win_size

        self.left_border_x = border_lines[0]
        self.right_border_x = border_lines[1]

        self.w = self.right_border_x - self.left_border_x
        self.h = rung_height_to_width_ratio * self.w

        first_time_span = time_span * start_y / height
        self.pos_anim = KFAnim((self.time, start_y), (self.time+first_time_span, 0))

        self.update_points(start_y)
    

post_height_to_width_ratio = 0.6

class ElectricityPost(InstructionGroup):
    
    def __init__(self, start_y, end_y, border_lines, wire_x):
        super(ElectricityPost, self).__init__()

        self.left_border_x = border_lines[0]
        self.right_border_x = border_lines[1]
        self.wire_x = wire_x

        self.w = self.right_border_x - self.left_border_x
        # self.h = post_height_to_width_ratio * self.w
        self.h = Window.height * post_height_ratio
        self.y_dist = end_y - start_y

        self.z = 0
        self.dz = 0

        x1, y1 = map_coords_3D_to_2D(self.left_border_x, start_y, self.z)   # bottom left
        x2, y2 = map_coords_3D_to_2D(self.left_border_x, start_y, self.z + self.h)   # top left
        x3, y3 = map_coords_3D_to_2D(self.right_border_x, start_y, self.z + self.h)   # top right
        x4, y4 = map_coords_3D_to_2D(self.right_border_x, start_y, self.z)   # bottom right

        self.post_color = Color(0, 0.39, 0, 0.1)
        self.post = Line(points=(x1, y1, x2, y2, x3, y3, x4, y4), width=3)
        self.add(self.post_color)
        self.add(self.post)

        self.points_input = np.linspace(-self.y_dist/2, self.y_dist/2, 100)
        z_wire = self.h - self.h*0.2*(1 - self.points_input**2 / (self.y_dist/2)**2)
        y_wire = self.points_input + start_y + self.y_dist/2

        self.wire_color = Color(0,0,0,0.1)
        self.add(self.wire_color)
        self.wires = []
        for i in range(len(self.wire_x)):
            points = []
            for j in range(len(self.points_input)):
                points += list(map_coords_3D_to_2D(self.wire_x[i], y_wire[j], self.z + z_wire[j]))
            self.wires.append(Line(points=points, width=2))
            self.add(self.wires[-1])

        self.time = 0
        self.anim = False

        first_time_span = time_span * (start_y+Window.height) / (Window.height)
        self.pos_anim = KFAnim((self.time, start_y), (self.time+first_time_span, -Window.height))

    def start_anim(self):
        self.anim = True

    def stop_anim(self):
        self.anim = False

    def switch_mode(self):
        if self.z == 0:
            self.dz = -dz
        elif self.z >= -Window.height * post_height_ratio:
            self.dz = dz

        if self.post_color.a == 0.1:
            self.post_color.a = 1
            self.wire_color.a = 1
        else:
            self.post_color.a = 0.1
            self.wire_color.a = 0.1

    def update_points(self, y):
        x1, y1 = map_coords_3D_to_2D(self.left_border_x, y, self.z)   # bottom left
        x2, y2 = map_coords_3D_to_2D(self.left_border_x, y, self.z + self.h)   # top left
        x3, y3 = map_coords_3D_to_2D(self.right_border_x, y, self.z + self.h)   # top right
        x4, y4 = map_coords_3D_to_2D(self.right_border_x, y, self.z)   # bottom right

        self.post.points = (x1, y1, x2, y2, x3, y3, x4, y4)

        z_wire = self.h - self.h*0.2*(1 - self.points_input**2 / (self.y_dist/2)**2)
        y_wire = self.points_input + y + self.y_dist/2

        for i in range(len(self.wire_x)):
            points = []
            for j in range(len(self.points_input)):
                points += list(map_coords_3D_to_2D(self.wire_x[i], y_wire[j], self.z + z_wire[j]))
            self.wires[i].points = points

        if y <= - Window.height:
            self.pos_anim = KFAnim((self.time, Window.height), (self.time+time_span*2, -Window.height))


    def on_update(self, dt):
        if self.dz < 0 and self.z > -Window.height * post_height_ratio:
            self.z = max(self.z + self.dz, -Window.height * post_height_ratio)
        elif self.dz > 0 and self.z < 0:
            self.z = min(self.z + self.dz, 0)
        else:
            self.dz = 0

        if self.anim:
            y = self.pos_anim.eval(self.time)
            self.update_points(y)
            self.time += dt


    def on_resize(self, win_size, start_y, end_y, border_lines):
        width, height = win_size

        self.left_border_x = border_lines[0]
        self.right_border_x = border_lines[1]
        self.y_dist = end_y - start_y

        self.points_input = np.linspace(-self.y_dist/2, self.y_dist/2, 100)
        self.w = self.right_border_x - self.left_border_x
        self.h = height * post_height_ratio

        first_time_span = time_span * (start_y+height) / (height)
        self.pos_anim = KFAnim((self.time, start_y), (self.time+first_time_span, -height))

        self.update_points(start_y)