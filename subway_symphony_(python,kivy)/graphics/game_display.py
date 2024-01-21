from imslib.gfxutil import topleft_label, CEllipse, KFAnim, AnimGroup, CRectangle, CLabelRect

from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Rectangle, Line, Quad
from kivy.graphics import PushMatrix, PopMatrix, Translate, Scale, Rotate

from kivy.core.window import Window
from kivy.clock import Clock

from helper_funcs import *
from player import *
from tracks import *
from obstacle import *
from coin import *
from train import *

from player import PlayerGraphics
from tracks import TracksGraphics
from obstacle import Obstacle
from train import Train
from improv_graphics import ImprovToken, ImprovIcon

import random

# NOTE:
# (1) 3d graphics?
# (2) sprites / textures for tracks / obstacles / player
# (3) shadow for jumping to help with locations
# (4) render obstacle above player after jumping
# (5) sync animation to the beat? that seems hard lol
# (6) extra graphical animation to the scene

class GameDisplay(InstructionGroup):
    
    def __init__(self, song_data, game_over_callback, piece):
        super(GameDisplay, self).__init__()

        # set up graphics
        self.tracks = TracksGraphics()
        self.objects = AnimGroup()
        self.objects.add(self.tracks)
        self.add(self.objects)

        self.player_graphics = PlayerGraphics(self.tracks)
        self.player_object = AnimGroup()
        self.player_object.add(self.player_graphics)
        # add object later

        self.nowbar_color = Color(0.25, 0.25, 0.25)
        self.nowbar_color.a = 0.2
        self.nowbar = Line(points = (0, self.player_graphics.nowbar_y, Window.width, self.player_graphics.nowbar_y), width=5)
        self.add(self.nowbar_color)
        self.add(self.nowbar)

        # TODO: set up gems based on song_data (SongData object)
        self.song_data = song_data
        self.piece = piece

        self.coins = [Coin(self.tracks, *i) for i in self.song_data.get_coin_data()]
        # for coin in self.coins:
        #     self.add(coin)
        # don't draw unnnecessary coins
        self.coin_idx_left = 0
        self.coin_idx_right = 0
        for i in range(len(self.coins)):
            coin = self.coins[i]
            if coin.time < 5:
                self.add(coin)
                self.coin_idx_right += 1
            else:
                break

        # print("num coins ", len(self.coins))

        self.obstacles = [Obstacle(self.tracks, *i) for i in self.song_data.get_obstacle_data()]
        # for i in self.obstacles:
        #     self.add(i)
        self.obstacle_idx = 0
        # don't draw unnecessary obstacles
        self.obstacle_idx_left = 0
        self.obstacle_idx_right = 0
        for i in range(len(self.obstacles)):
            obstacle = self.obstacles[i]
            if obstacle.time < 5:
                self.add(obstacle)
                self.obstacle_idx_right += 1

        # print("num obstacles ", len(self.obstacles))

        self.trains = [Train(self.tracks, *i) for i in self.song_data.get_train_data()]
        # for i in self.trains:
        #     print(i.end_time)
        self.train_idx = 0
        self.active_trains = set()

        self.train_idx_left = 0
        self.train_idx_right = 0

        for i in range(len(self.trains)):
            train = self.trains[i]
            if train.start_time < 5:
                self.add(train)
                self.train_idx_right += 1

        # add improv graphics

        # collectible improv token
        if self.piece == "Trepak":
            self.improv_token = ImprovToken(self.tracks, lane=random.randint(0, 2), time=12.43+2.337) # 12.467 is on beat
        elif self.piece == "Waltz":
            self.improv_token = ImprovToken(self.tracks, lane=random.randint(0, 2), time=19.7)
        self.add(self.improv_token)
        # graphical feedback during improv
        self.improv_icon = ImprovIcon()
        self.mode = 'reg'

        # add player graphics
        self.add(self.player_object)

        self.posts = self.tracks.get_posts()
        for post in self.posts:
            self.add(post)

        self.instrument_icon = InstrumentIcon()
        self.add(self.instrument_icon)

        # text left for debugging purposes
        self.debug_text = CLabelRect(cpos=(Window.width*0.2, Window.height*0.9), text="")
        self.add(self.debug_text)

        self.font_size = Window.width * 0.03

        # handle score display
        self.score = 0
        self.score_color = Color(0,0,0)
        self.score_label = CLabelRect((100,100), text='Score: ' + str(self.score), font_name='Gemstone.ttf', font_size=self.font_size * 0.7)
        self.score_label_y = Window.height*0.8
        self.score_label.cpos = (Window.width*0.8, self.score_label_y)
        self.add(self.score_color)
        self.add(self.score_label)

        # handle streak display
        self.streak = 0
        self.streak_border_color = Color(0,0,0)
        self.streak_color = Color(1,1,1)
        self.streak_label_border = CLabelRect((Window.width*0.33,Window.width*0.33), text=f'{self.streak}', font_name='Gemstone.ttf', font_size=self.font_size)
        self.streak_label = CLabelRect((Window.width*0.3,Window.width*0.3), text=f'{self.streak}', font_name='Gemstone.ttf', font_size=self.font_size*0.88)
        self.streak_label_border.cpos = (Window.width*0.5, Window.height*0.86)
        self.streak_label.cpos = (Window.width*0.5, Window.height*0.86)
        self.add(self.streak_border_color)
        self.add(self.streak_label_border)
        self.add(self.streak_color)
        self.add(self.streak_label)

        # function to call when game is over
        # currently called by the game_screen, but probably should be called by player
        self.game_over_callback = game_over_callback
        self.game_over = False

        self.collide_callback = None
        self.collision_check_on = True

        self.tracks.start_anim()
        self.playing = True
        # self.playing = False
        self.player_graphics.start_running()
    
    def toggle_playing(self):
        self.playing = True

    def set_collide_callback(self, collide_callback):
        self.collide_callback = collide_callback

    def switch_mode(self):
        self.tracks.switch_mode()
        for i in range(len(self.trains)):
            self.trains[i].switch_mode(self.train_idx_left <= i <= self.train_idx_right)
        for i in range(len(self.obstacles)):
            self.obstacles[i].switch_mode(self.obstacle_idx_left <= i < self.obstacle_idx_right)

        if self.mode == 'reg':
            self.mode = 'improv'
            self.player_graphics.stop_running()
            self.add(self.improv_icon)
            self.remove(self.instrument_icon)
            self.remove(self.streak_border_color)
            self.remove(self.streak_label_border)
            self.remove(self.streak_color)
            self.remove(self.streak_label)
            self.toggle_collision_check(0)
            for coin in self.coins:
                coin.color.a = 0
                coin.shadow_color.a = 0
        else:
            self.mode = 'reg'
            self.player_graphics.start_running()
            self.remove(self.improv_icon)
            self.add(self.instrument_icon)
            self.add(self.streak_border_color)
            self.add(self.streak_label_border)
            self.add(self.streak_color)
            self.add(self.streak_label)
            Clock.schedule_once(self.toggle_collision_check, 2)
            for coin in self.coins:
                coin.color.a = 1
                coin.shadow_color.a = 0.25


    def on_key_down(self, keycode, modifiers):
        # play / pause toggle
        # if keycode[1] == 'p':
        #     if self.playing:
        #         self.tracks.stop_anim()
        #         self.playing = False
        #         self.player_graphics.stop_running()
        #     else:
        #         self.tracks.start_anim()
        #         self.playing = True
        #         self.player_graphics.start_running()
        
        # get player action
        if keycode[1] == 'left':
            self.player_graphics.switch_lanes(False)
        if keycode[1] == 'right':
            self.player_graphics.switch_lanes(True)
        if keycode[1] == 'up':
            self.player_graphics.jump()
        
        # NOTE: force screen change during development
        # TODO: change to game over condition
        if keycode[1] == 'q':
            self.playing = False

    def toggle_collision_check(self, dt):

        print("toggled")
        self.collision_check_on = not self.collision_check_on

    def collision_check_train_side(self):
        # only called when switching lanes
        # collision conditions for the side of train
        # (1) player is in the same lane as train
        # (2) player's lowest y_position at the moment 

        collision = False

        current_lane = self.player_graphics.get_lane()
        # next_lane = self.player_graphics.next_lane

        if current_lane != None:
            for train in self.active_trains:

                # if next_lane == train.lane and current_lane != next_lane:
                if current_lane == train.lane and self.player_graphics.velocity[0] != 0:
                    collision = True
                    self.collide_callback()
                    break
        
        return collision
    
    
    def collision_check_obstacle(self):
        
        # collision conditions for obstacle:
        # (1) player is in the same lane as obstacle
        # (2) player's lowest y_position at the moment is not above the obstacle

        collision = False

        # check if there is an obstacle in the lane
        # current_lane = self.player_graphics.lane
        current_lane = self.player_graphics.get_lane()
        obstacle = self.obstacles[self.obstacle_idx] # next obstacle
        foot_height = self.player_graphics.get_foot_y_pos()

        if current_lane != None:
            if current_lane == obstacle.lane:
                if foot_height < obstacle.get_perceived_height():
                    collision = True
        
        return collision
    
    def collision_check_train_front(self):
        
        # collision conditions for the front of train
        # (1) player is in the same lane as train
        # (2) player's lowest y_position at the moment is not above the train

        collision = False

        current_lane = self.player_graphics.get_lane()
        foot_height = self.player_graphics.get_foot_y_pos()
        for train in self.active_trains:

            if current_lane == train.lane and train.get_train_y_pos()[0] <= foot_height:
                collision = True
                break
        
        return collision
    
    def set_score(self, score):
        self.score = score
    
    def set_streak(self, streak):
        self.streak = streak

    def on_game_over(self):
        self.player_graphics.on_game_over()
        self.tracks.stop_anim()
        self.game_over_callback()
        self.mode = 'reg'


    def on_update(self, now_time):
        # manage graphics
        self.objects.on_update()
        self.player_object.on_update()

        # now_time = now_time - 3

        if self.playing:

            # manage range of obstacles to be displayed
            while self.obstacle_idx_left < len(self.obstacles) and self.obstacles[self.obstacle_idx_left].time < now_time-1:
                self.remove(self.obstacles[self.obstacle_idx_left])
                self.obstacle_idx_left += 1
            while self.obstacle_idx_right < len(self.obstacles) and self.obstacles[self.obstacle_idx_right].time < now_time + 5:
                self.add(self.obstacles[self.obstacle_idx_right])
                self.obstacle_idx_right += 1
            for i in range(self.obstacle_idx_left, self.obstacle_idx_right):
                self.obstacles[i].on_update(now_time)
            # for obstacle in self.obstacles:
            #     obstacle.on_update(now_time)

            # manage range of trains to be displayed
            # print(self.train_idx_left, self.train_idx_right)
            # while self.train_idx_left < len(self.trains) and self.trains[self.train_idx_left].end_time < now_time -1:
            #     self.remove(self.trains[self.train_idx_left])
            #     self.train_idx_left += 1
            while self.train_idx_right < len(self.trains) and self.trains[self.train_idx_right].start_time < now_time + 5:
                self.add(self.trains[self.train_idx_right])
                self.train_idx_right += 1
            last_removed = 0
            for i in range(self.train_idx_left, self.train_idx_right):
                if self.trains[i].end_time < now_time - 2:
                    self.remove(self.trains[i])
                    last_removed = i
                else:
                    self.trains[i].on_update(now_time)
            self.train_idx_left = last_removed

            # for train in self.trains:
            #     train.on_update(now_time)
            
            # for coin in self.coins:
            #     coin.on_update(now_time)

            # manage range of coins to be displayed
            while self.coins[self.coin_idx_left].time < now_time-1:
                self.remove(self.coins[self.coin_idx_left])
                # print('here')
                self.coin_idx_left += 1
            while self.coin_idx_right < len(self.coins) and self.coins[self.coin_idx_right].time < now_time+5:
                self.add(self.coins[self.coin_idx_right])
                self.coin_idx_right += 1
            for i in range(self.coin_idx_left, self.coin_idx_right):
                self.coins[i].on_update(now_time)
        
        self.remove(self.player_object)
        self.add(self.player_object)

        # redraw obstacles that have passed to give a sense of depth
        for i in range(self.obstacle_idx_left, self.obstacle_idx_right):
            obstacle = self.obstacles[i]
            if obstacle.time < now_time:
                self.remove(obstacle)
                self.add(obstacle)

        # # redraw trains that have passed to give a sense of depth
        # for train in self.trains:
        #     if train.end_time < now_time:
        #         self.remove(train)
        #         self.add(train)
        for i in range(self.train_idx_left, self.train_idx_right):
            train = self.trains[i]
            if train.end_time < now_time:
                self.remove(train)
                self.add(train)
        
        if self.playing:
            self.improv_token.on_update(now_time)
            self.instrument_icon.on_update(now_time)

        # if not self.playing:
        #     self.debug_text.set_text('press p to start the game')
        # else:
        #     self.debug_text.set_text("")

        # check collision at the moment an obstacle is being passed in time
        if self.collision_check_on and self.obstacle_idx < len(self.obstacles) and self.obstacles[self.obstacle_idx].time <= now_time:
            collision = self.collision_check_obstacle()
            if self.mode == 'reg' and collision:
                print("collision with obstacle ", self.obstacle_idx)
                self.game_over = True
            self.obstacle_idx += 1

        if self.collision_check_on:
            if self.mode == 'reg':
                if self.collision_check_train_side():
                    print("HIT THE SIDE TRAIN")
                    self.player_graphics.on_train_side_collision()
                elif self.collision_check_train_front():
                    print("collision with train")
                    self.game_over = True


        # manage self.active trains
        # step 1: remove trains that are over
        to_remove = []
        for train in self.active_trains:
            if train.end_time <= now_time:
                to_remove.append(train)
        for train in to_remove:
            self.active_trains.remove(train)
        # step 2: add trains that just started
        if self.train_idx < len(self.trains) and self.trains[self.train_idx].start_time <= now_time:
            self.active_trains.add(self.trains[self.train_idx])
            self.train_idx += 1

        self.score_label.set_text('Score: ' + str(self.score))
        self.streak_label_border.set_text(f'{self.streak}')
        self.streak_label.set_text(f'{self.streak}')

        if self.game_over:
            self.on_game_over()
            self.game_over = False
    
        if self.mode == 'improv':
            self.improv_icon.on_update(now_time)
        

    def on_resize(self, win_size):
        self.tracks.on_resize(win_size)
        for train in self.trains:
                train.on_resize(win_size)
        for obstacle in self.obstacles:
            obstacle.on_resize(win_size)
        for coin in self.coins:
            coin.on_resize(win_size)
        self.player_graphics.on_resize(win_size)
        self.instrument_icon.on_resize(win_size)
        self.improv_token.on_resize(win_size)
        self.improv_icon.on_resize(win_size)

        self.font_size = win_size[0]*0.03

        self.score_label.set_font_size(self.font_size * 0.7)
        self.score_label.set_cpos((win_size[0]*0.8, win_size[1]*0.8))

        self.streak_label_border.set_font_size(self.font_size)
        self.streak_label.set_font_size(self.font_size*0.88)
        self.streak_label_border.set_cpos((win_size[0]*0.5, win_size[1]*0.86))
        self.streak_label.set_cpos((win_size[0]*0.5, win_size[1]*0.86))

        self.nowbar.points = (0, self.player_graphics.nowbar_y, win_size[0], self.player_graphics.nowbar_y)