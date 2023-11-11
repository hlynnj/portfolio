#####################################################################
#
# This software is to be used for MIT's class Interactive Music Systems only.
# Since this file may contain answers to homework problems, you MAY NOT release it publicly.
#
#####################################################################

import sys, os
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('./unit6'))

from imslib.core import BaseWidget, run, lookup
from imslib.audio import Audio
from imslib.mixer import Mixer
from imslib.wavegen import WaveGenerator
from imslib.wavesrc import WaveBuffer, WaveFile

from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Line, Rectangle
from imslib.gfxutil import topleft_label, CEllipse, CRectangle, KFAnim, AnimGroup, CLabelRect
from kivy.core.window import Window

class MainWidget(BaseWidget):
    def __init__(self):
        super(MainWidget, self).__init__()

        self.song_data = SongData()
        self.audio_ctrl = AudioController()
        self.display = GameDisplay(self.song_data)
        self.player = Player(self.song_data, self.audio_ctrl, self.display)

        self.canvas.add(self.display)

        self.info = topleft_label()
        self.add_widget(self.info)

    def on_key_down(self, keycode, modifiers):
        # play / pause toggle
        if keycode[1] == 'p':
            self.audio_ctrl.toggle()

        # button down
        button_idx = lookup(keycode[1], '12345', ("1","2","3","4","5"))
        if button_idx != None:
            # print('down', button_idx)
            self.display.on_button_down(button_idx)
            self.player.on_button_down(button_idx)

    def on_key_up(self, keycode):
        # button up
        button_idx = lookup(keycode[1], '12345', ("1","2","3","4","5"))
        if button_idx != None:
            # print('up', button_idx)
            self.display.on_button_up(button_idx)
            self.player.on_button_up(button_idx)

    # handle changing displayed elements when window size changes
    # This function should call GameDisplay.on_resize
    def on_resize(self, win_size):
        
        self.display.on_resize(win_size)

    def on_update(self):
        self.audio_ctrl.on_update()

        now = self.audio_ctrl.get_time()  # time of song in seconds.
        self.display.on_update(now)
        self.player.on_update(now)

        self.info.text = 'p: pause/unpause song\n'
        self.info.text += f'song time: {now:.2f}\n'
        self.info.text += f'num objects: {self.display.get_num_object()}\n'


# Handles everything about Audio.
#   creates the main Audio object
#   load and plays solo and bg audio tracks
#   creates audio buffers for sound-fx (miss sound)
#   functions as the clock (returns song time elapsed)
class AudioController(object):
    def __init__(self):
        super(AudioController, self).__init__()
        self.audio = Audio(2)
        self.mixer = Mixer()
        self.audio.set_generator(self.mixer)

        # song
        self.backing = WaveGenerator(WaveFile("./unit6/class6/data/KillerQueen_bg.wav"))
        self.solo = WaveGenerator(WaveFile("./unit6/class6/data/KillerQueen_solo.wav"))
        self.mixer.add(self.backing)
        self.mixer.add(self.solo)

        # start tracks paused
        self.backing.pause()
        self.solo.pause()

    # start / stop the song
    def toggle(self):
        self.backing.play_toggle()
        self.solo.play_toggle()

    # mute / unmute the solo track
    def set_mute(self, mute):
        if mute:
            print("muted")
            self.solo.set_gain(0)
        else:
            print("unmuted")
            self.solo.set_gain(1)

    # play a sound-fx (miss sound)
    def play_miss(self):
        pass

    # return current time (in seconds) of song
    def get_time(self):
        return self.backing.frame / Audio.sample_rate

    # needed to update audio
    def on_update(self):
        self.audio.on_update()


# Holds data for gems and barlines.
# From Lab 6

# for parsing gem text file: return (time, lane) from a single line of text
def beat_from_line(line):
    time, beat = line.strip().split('\t')
    return (float(time), int(beat))
    
class SongData(object):
    def __init__(self):
        super(SongData, self).__init__()

        # solo song data
        self.gem_beats = []
        gem_file = './unit6/class6/data/KillerQueen_gems.txt'
        gem_lines = open(gem_file).readlines()
        self.gem_beats = [beat_from_line(l) for l in gem_lines]

        # hold song data
        self.hold_beats = []
        hold_file = './unit6/class6/data/KillerQueen_holds.txt'
        hold_lines = open(hold_file).readlines()
        for i in range(0, len(hold_lines), 2):
            start_time, lane = hold_lines[i].strip().split('\t')
            end_time, _ = hold_lines[i+1].strip().split('\t')
            self.hold_beats.append((float(start_time), float(end_time), int(lane)))

        # backing track song data
        self.beats = []
        backing_file = './unit6/class6/data/KillerQueen_beats.txt'
        backing_lines = open(backing_file).readlines()
        self.beats = [beat_from_line(l) for l in backing_lines]

    def get_gem_beats(self):
        return self.gem_beats

    def get_hold_beats(self):
        return self.hold_beats
    
    def get_backing_beats(self):
        return self.beats


def lines_from_file(filename):
    lines = []
    with open(filename, encoding="utf-8") as f:
        for line in f:
            lines.append(line)
    return lines


# configuration parameters:
nowbar_h = 0.2
nowbar_w_margin = 0.1
time_span = 2.0
beat_marker_len = 0.2

# convert a time value to a y-pixel value (where time==0 is on the nowbar)
def time_to_ypos(time):
    y_ratio = (time / time_span)
    nowbar = Window.height * nowbar_h
    y_pos = nowbar + Window.height * (y_ratio)
    return int(y_pos) # my laptop has window_size == 900 :((

# Display for a single gem at a position with a hue or color
class GemDisplay(InstructionGroup):
    def __init__(self, lane, time, color):
        super(GemDisplay, self).__init__()

        self.time = time  # the timestamp (in seconds) of this beat
        self.color = color # color of this beat line
        self.lane = lane # lane of this gem

        self.r = int(Window.width / 25)

        self.y_pos = Window.height + self.r
        self.x_pos = int(Window.width * (0.2 + 0.1*int(lane)))

        self.add(self.color)
        self.gem = CEllipse(cpos=(self.x_pos, self.y_pos), csize=(self.r,self.r))
        self.add(self.gem)

    # change to display this gem being hit
    def on_hit(self):
        self.color.s = 0.25

    # change to display a passed or missed gem
    def on_pass(self):
        self.color.a -= 0.5

    # animate gem (position and animation) based on current time
    def on_update(self, now_time):
        
        if now_time == 0 or now_time < self.time - time_span or now_time > self.time + time_span:
            return False
        
        y_pos = time_to_ypos(self.time - now_time)
        self.gem.set_cpos((self.x_pos, y_pos))
        return True

    def on_resize(self, win_size):

        self.r = int(win_size[0] / 25)
        self.y_pos = win_size[1] + self.r
        self.x_pos = int(win_size[0] * (0.2 + 0.1*int(self.lane)))
        self.gem.cpos = (self.x_pos, self.y_pos)
        self.gem.csize = (self.r,self.r)


# Child of HoldDisplay, represents the falling bar in between the start and end gems
class FallingRect(InstructionGroup):
    def __init__(self, lane, time, duration, color):
        super(FallingRect, self).__init__()

        self.lane = lane
        self.time = time
        self.duration = duration
        self.color = color

        self.r = int(Window.width / 25)
        self.width = self.r
        self.original_height = int(Window.height * self.duration / time_span)
        self.height = self.original_height

        self.y_pos = Window.height
        self.x_pos = int(Window.width * (0.2 + 0.1*int(lane)))

        self.add(self.color)
        self.rect = Rectangle(pos=(self.x_pos - self.r/2, self.y_pos), size=(self.width, self.height))
        self.add(self.rect)

        self.hit = False
        self.passed = False

    # animate gem (position and animation) based on current time
    def on_update(self, now_time):
        
        if now_time == 0 or now_time < self.time - time_span or now_time > self.time + self.duration + time_span:
            return False
        
        y_pos = time_to_ypos(self.time - now_time)

        # keep falling
        if y_pos > Window.height * nowbar_h:
            self.rect.pos = (self.x_pos - self.r/2, y_pos)
        # start shrinking
        elif self.hit:
            self.height = max(0, int(self.original_height * (1 - ((now_time - self.time) / self.duration))))
            self.rect.pos = (self.x_pos - self.r/2, int(Window.height * nowbar_h))
            self.rect.size = (self.width, self.height)
        elif not self.hit:
            if self.passed:
                self.rect.pos = (self.x_pos - self.r/2, y_pos + self.original_height - self.height)
            else:
                self.rect.pos = (self.x_pos - self.r/2, y_pos)

        return True

    def on_resize(self, win_size):
        
        self.y_pos = int(self.y_pos * win_size[1] / Window.height)
        self.x_pos = int(win_size[0] * (0.2 + 0.1*int(self.lane)))
        self.r = int(win_size[0] / 25)
        self.width = self.r
        self.rect.pos = (self.x_pos - self.r/2, self.y_pos)

        self.original_height = int(win_size[1] * self.duration / time_span)
        self.height = self.original_height
        self.rect.size = (self.width, self.height)


# Display for a single hold-type gem at a position with a hue or color
class HoldDisplay(InstructionGroup):
    def __init__(self, lane, time, duration, color):
        super(HoldDisplay, self).__init__()

        self.time = time  # the timestamp (in seconds) of this beat
        self.color = color # color of this beat line
        self.lane = lane # lane of this gem
        self.duration = duration

        self.start_gem = GemDisplay(self.lane, self.time, Color(rgba=color.rgba))
        self.rect = FallingRect(self.lane, self.time, self.duration, Color(rgba=color.rgba))
        self.end_gem = GemDisplay(self.lane, self.time + self.duration, Color(rgba=color.rgba))

        self.add(self.start_gem)
        self.add(self.rect)
        self.add(self.end_gem)

    def on_start(self):
        self.rect.color.h = 0.9
        self.end_gem.color.h = 0.9
        self.rect.hit = True
        self.start_gem.color.a = 0

    def on_end(self):
        self.color.a = 0
        self.end_gem.color.a = 0

    # change to display a passed or missed gem
    def on_pass(self):
        self.rect.hit = False
        self.rect.passed = True
        self.start_gem.color.a = 0.5
        self.rect.color.a = 0.5
        self.end_gem.color.a = 0.5

    # animate gem (position and animation) based on current time
    def on_update(self, now_time):
        
        if now_time == 0 or now_time < self.time - time_span or now_time > self.time + self.duration + time_span:
            return False
        
        self.start_gem.on_update(now_time)
        self.rect.on_update(now_time)
        self.end_gem.on_update(now_time)

        return True
    
    def on_resize(self, win_size):
        
        self.start_gem.on_resize(win_size)
        self.rect.on_resize(win_size)
        self.end_gem.on_resize(win_size)


# Displays a single barline on screen
class BarlineDisplay(InstructionGroup):
    def __init__(self, time):
        super(BarlineDisplay, self).__init__()
        self.time = time  # the timestamp (in seconds) of this beat

        self.color = Color(rgb=(1, 1, 1))
        self.color.a = 0.5
        self.line = Line(width=3)
        self.line.points = (0, 0, Window.width, 0)

        self.add(self.color)
        self.add(self.line)

    # animate barline (position) based on current time
    def on_update(self, now_time):
        
        if now_time == 0 or now_time < self.time - time_span or now_time > self.time + time_span:
            return False
        
        y_pos = time_to_ypos(self.time - now_time)
        self.line.points = (0, y_pos, Window.width, y_pos)
        return True


# Displays one button on the nowbar
class ButtonDisplay(InstructionGroup):
    def __init__(self, lane, color):
        super(ButtonDisplay, self).__init__()

        self.lane = lane
        self.color = color

        # lane = "1", "2", "3", "4", or "5"
        self.x_pos = int(Window.width * (0.2 + 0.1*int(lane)))
        self.y_pos = int(Window.height * nowbar_h)
        self.r = int(Window.width/25)

        self.add(self.color)
        self.button = CEllipse(cpos=(self.x_pos, self.y_pos), csize=(self.r, self.r))
        self.add(self.button)

    # displays when button is pressed down
    def on_down(self):
        self.color.a = 1

    # back to normal state
    def on_up(self):
        self.color.a = 0.7

    # modify object positions based on new window size
    def on_resize(self, win_size):
        
        self.x_pos = int(win_size[0] * (0.2 + 0.1*int(self.lane)))
        self.y_pos = int(win_size[1] * nowbar_h)
        self.r = int(win_size[0]/25)

        self.button.cpos = (self.x_pos, self.y_pos)
        self.button.csize = (self.r, self.r)

# Displays nowbar
class NowBar(InstructionGroup):
    def __init__(self, color):
        super(NowBar, self).__init__()
        self.color = color

        self.line = Line(width=3)
        self.left = (int(Window.width*nowbar_w_margin), int(Window.height*nowbar_h))
        self.right = (int(Window.width*(1-nowbar_w_margin)), int(Window.height*nowbar_h))
        self.line.points = (*self.left, *self.right)

        self.add(self.color)
        self.add(self.line)

    # modify object positions based on new window size
    def on_resize(self, win_size):
        
        self.left = (int(win_size[0]*nowbar_w_margin), int(win_size[1]*nowbar_h))
        self.right = (int(win_size[0]*(1-nowbar_w_margin)), int(win_size[1] * nowbar_h))
        self.line.points = (*self.left, *self.right)
                    
# Displays one lane line
class LaneLine(InstructionGroup):
    def __init__(self, lane, color):
        super(LaneLine, self).__init__()
        self.color = color
        self.lane = lane
        self.x_pos = int(Window.width * (0.2 + 0.1*int(lane)))

        self.line = Line(width=1)
        self.line.points = (self.x_pos, int(Window.height*nowbar_h), self.x_pos, Window.height)

        self.add(self.color)
        self.add(self.line)

    # modify object positions based on new window size
    def on_resize(self, win_size):
        
        self.x_pos = int(win_size[0] * (0.2 + 0.1*int(self.lane)))
        self.line.points = (self.x_pos, int(win_size[1]*nowbar_h), self.x_pos, win_size[1])

class HitCircle(InstructionGroup):
    def __init__(self, cpos, start_radius, end_radius, duration, color):
        super(HitCircle, self).__init__()

        self.cpos = cpos
        self.start_radius = start_radius
        self.end_radius = end_radius
        self.duration = duration

        self.grow_anim = KFAnim((0, start_radius), (duration, end_radius))

        self.color = color
        self.add(self.color)

        self.line = Line(width = 1)
        self.line.circle = (self.cpos[0], self.cpos[1], start_radius)

        self.add(self.line)

        self.start_time = 0
        self.time = 0
        self.on_update(0)
    
    def on_update(self, time):
        if not self.start_time:
            self.start_time = time
        
        dt = time - self.start_time

        radius = self.grow_anim.eval(self.time)

        self.color.a = 1-(self.time/self.duration)
        self.line.circle = (self.cpos[0], self.cpos[1], radius)

        self.time += dt

        return self.time < self.duration


# Displays all game elements: nowbar, buttons, barlines, gems
class GameDisplay(InstructionGroup):
    def __init__(self, song_data):
        super(GameDisplay, self).__init__()

        # gems
        self.solo_data = song_data.get_gem_beats()
        self.solo_beats = [GemDisplay(lane=b[1], time=b[0], color=Color(rgba=(0, 1, 0, 1))) for b in self.solo_data]
        for b in self.solo_beats:
            self.add(b)
        
        # hold gems
        self.hold_data = song_data.get_hold_beats()
        self.hold_beats = [HoldDisplay(lane=b[2], time=b[0], duration=b[1]-b[0], color=Color(rgba=(0, 0, 1, 1))) for b in self.hold_data]
        for b in self.hold_beats:
            self.add(b)
        
        # beat lines
        self.backing_data = song_data.get_backing_beats()
        self.backing_beats = [BarlineDisplay(time=b[0]) for b in self.backing_data]
        for b in self.backing_beats:
            self.add(b)
        
        # buttons
        self.buttons = {}
        for lane in "12345":
            button = ButtonDisplay(lane, color=Color(rgba=(1,1,1,0.7)))
            self.buttons[lane] = button
            self.add(button)

        # nowbar
        self.nowbar = NowBar(Color(rgb=(1,1,1)))
        self.add(self.nowbar)

        # lane lines
        self.lane_lines = []
        for lane in "12345":
            lane_line = LaneLine(lane, color=Color(rgba=(1, 1, 1, 0.7)))
            self.lane_lines.append(lane_line)
            self.add(lane_line)
        
        # hit circles
        self.hit_circles = []

        # hold displays
        self.rects = []

        # score display
        self.score = 0
        self.scoreboard = CLabelRect(cpos=(Window.width * 0.07, Window.height * 0.80), text=f'SCORE: {self.score}', font_size=21)
        self.combo = 0
        self.comboboard = CLabelRect(cpos=(Window.width * 0.07, Window.height * 0.75), text=f'COMBO: {self.combo}', font_size=21)

        self.add(self.scoreboard)
        self.add(self.comboboard)

    # called by Player when succeeded in hitting this gem.
    def gem_hit(self, gem_idx):
        # remove hit gem
        self.solo_beats[gem_idx].color.a = 0

        # add a growing circle to indicate hit
        lane = self.solo_data[gem_idx][1]
        x_pos = int(Window.width * (0.2 + 0.1*int(lane)))
        y_pos = int(Window.height * nowbar_h)
        hit_circle = HitCircle(cpos=(x_pos,y_pos), start_radius=int(Window.width/25.5), end_radius=int(Window.width/23), duration=2, color=Color(rgba=(1, 1, 1, 0.8)))
        self.add(hit_circle)
        self.hit_circles.append(hit_circle)

    # called by Player on pass or miss.
    def gem_pass(self, gem_idx):
        # change missed gem
        self.solo_beats[gem_idx].color.a = 0.4
    
    def hold_start(self, gem_idx):

        self.hold_beats[gem_idx].on_start()
    
    def hold_end(self, gem_idx):

        self.hold_beats[gem_idx].on_end()
    
    def hold_pass(self, gem_idx):

        self.hold_beats[gem_idx].on_pass()

    # called by Player on button down
    def on_button_down(self, lane):
        self.buttons[lane].on_down()

    # called by Player on button up
    def on_button_up(self, lane):
        self.buttons[lane].on_up()

    # called by Player to update score
    def set_score(self, score):
        self.score = score
        self.scoreboard.set_text(f'SCORE: {self.score}')
    
    def set_combo(self, combo):
        self.combo = combo
        self.comboboard.set_text(f'COMBO: {self.combo}')

    # for when the window size changes
    def on_resize(self, win_size):
        
        for b in self.solo_beats:
            b.on_resize(win_size)
        
        for b in self.hold_beats:
            b.on_resize(win_size)
        
        for b in self.buttons:
            self.buttons[b].on_resize(win_size)
        
        self.nowbar.on_resize(win_size)

        for l in self.lane_lines:
            l.on_resize(win_size)
    
    def get_num_object(self):
        return len(self.children)

    # call every frame to handle animation needs
    def on_update(self, now_time):

        barline_to_remove = []
        barline_to_add = []
        
        for b in self.backing_beats:
            vis = b.on_update(now_time)
            # Part 5
            if not vis:
                barline_to_remove.append(b)
            else:
                barline_to_add.append(b)
        
        for b in barline_to_remove:
            if b in self.children:
                self.remove(b)
        
        for b in barline_to_add:
            if b not in self.children:
                self.add(b)

        gem_to_remove = []
        gem_to_add = []
        
        for g in self.solo_beats:
            vis = g.on_update(now_time)
            # Part 5
            if not vis:
                gem_to_remove.append(g)
            else:
                gem_to_add.append(g)
        
        for g in gem_to_remove:
            if g in self.children:
                self.remove(g)
        
        for g in gem_to_add:
            if g not in self.children:
                self.add(g)
        
        circle_to_remove = []

        for c in self.hit_circles:
            vis = c.on_update(now_time)
            if not vis:
                circle_to_remove.append(c)
        for c in circle_to_remove:
            if c in self.children:
                self.remove(c)
        
        rect_to_remove = []
        rect_to_add = []
        
        for r in self.hold_beats:
            vis = r.on_update(now_time)
            # Part 5
            if not vis:
                rect_to_remove.append(r)
            else:
                rect_to_add.append(r)
        
        for r in rect_to_remove:
            if r in self.children:
                self.remove(r)
        
        for r in rect_to_add:
            if r not in self.children:
                self.add(r)

# Handles game logic and keeps track of score.
# Controls the GameDisplay and AudioCtrl based on what happens
class Player(object):
    def __init__(self, song_data, audio_ctrl, display):
        super(Player, self).__init__()

        self.solo_data = song_data
        self.audio_ctrl = audio_ctrl
        self.display = display

        self.gems = self.solo_data.get_gem_beats()

        self.holds = self.solo_data.get_hold_beats()

        self.gem_map = {idx: False for idx in range(len(self.gems))} # is hit?
        self.gem_map_lane = {idx: False for idx in range(len(self.gems))} # is lane missed?

        self.active_gem_left = 0
        self.active_gem_right = 0

        self.hold_map = {idx: False for idx in range(len(self.holds))} # is hit?
        self.hold_map_lane = {idx: False for idx in range(len(self.holds))} # is lane missed?

        self.hold_active_gem_left = 0
        self.hold_active_gem_right = 0

        self.current_hold = 0
        self.time = 0

        self.multiplier = 1.5
        self.hit_score = 200
        self.score = 0
        self.combo = 0

    # called by MainWidget
    def on_button_down(self, lane):
        
        seen_lanes = set()
        for i in range(self.active_gem_left, self.active_gem_right):
            # case 1: gem hit
            if self.gems[i][1] == int(lane) and not self.gem_map[i]:
                print("hit gem no. ", i)
                self.gem_map[i] = True
                self.display.gem_hit(i)
                self.audio_ctrl.set_mute(False)
                self.score += self.hit_score * self.multiplier
                self.display.set_score(self.score)
                self.combo += 1
                self.display.set_combo(self.combo)
            seen_lanes.add(self.gems[i][1])
        
        for i in range(self.hold_active_gem_left, self.hold_active_gem_right):
            # case 2: hold hit
            if self.holds[i][2] == int(lane) and not self.hold_map[i]:
                print("hit hold no. ", i)
                self.hold_map[i] = True
                self.display.hold_start(i)
                self.audio_ctrl.set_mute(False)
                self.current_hold = i
                self.score += self.hit_score * self.multiplier
                self.display.set_score(self.score)
                self.combo += 1
                self.display.set_combo(self.combo)
            seen_lanes.add(self.holds[i][2])
        
        # case 3: temporal miss
        if len(seen_lanes) == 0:
            print("temporal miss")
            self.audio_ctrl.set_mute(True)
            self.multiplier = max(1, self.multiplier - 0.03)
            self.combo = 0
            self.display.set_combo(self.combo)

        # case 4: lane miss
        elif int(lane) not in seen_lanes:

            if self.active_gem_left < len(self.gems) or self.hold_active_gem_left < len(self.hold):

                if (self.active_gem_left < len(self.gems) and self.hold_active_gem_left < len(self.holds) and self.gems[self.active_gem_left][0] < self.holds[self.hold_active_gem_left][0]) or not self.hold_active_gem_left < len(self.holds):
                    print("lane miss gem: ", self.active_gem_left)
                    self.display.gem_pass(self.active_gem_left)
                    self.gem_map_lane[self.active_gem_left] = True
                
                elif self.hold_active_gem_left < len(self.holds):
                    print("lane miss hold: ", self.hold_active_gem_left)
                    self.display.hold_pass(self.hold_active_gem_left)
                    self.hold_map_lane[self.hold_active_gem_left] = True
                
                self.audio_ctrl.set_mute(True)
                self.multiplier = max(1, self.multiplier - 0.03)
                self.combo = 0
                self.display.set_combo(self.combo)


    # called by MainWidget
    def on_button_up(self, lane):
        
        if self.holds[self.current_hold][2] == int(lane) and self.hold_map[self.current_hold]:
            # case 5: hold end hit
            if self.holds[self.current_hold][1] > self.time - 0.1 and self.holds[self.current_hold][1] < self.time + 0.1:
                print("hold end gem no. ", self.current_hold)
                self.display.hold_end(self.current_hold)
                self.audio_ctrl.set_mute(False)
                self.score += self.hit_score * self.multiplier
                self.hold_map[self.current_hold] = False
                self.display.set_score(self.score)
                self.combo += 1
                self.display.set_combo(self.combo)
            # case 6: hold end pass
            else:
                print("pass hold end no. ", self.current_hold)
                self.display.hold_pass(self.current_hold)
                self.audio_ctrl.set_mute(True)
                self.multiplier = max(1, self.multiplier - 0.03)
                self.hold_map[self.current_hold] = False
                self.combo = 0
                self.display.set_combo(self.combo)

    # needed to check for pass gems (ie, went past the slop window)
    def on_update(self, time):

        self.time = time

        while self.active_gem_left < len(self.gems) and self.gems[self.active_gem_left][0] < time - 0.1:
            # case 7: gem pass
            if not self.gem_map[self.active_gem_left] and not self.gem_map_lane[self.active_gem_left]:
                print("pass gem no. ", self.active_gem_left)
                self.display.gem_pass(self.active_gem_left)
                self.audio_ctrl.set_mute(True)
                self.multiplier  = max(1, self.multiplier - 0.03)
                self.combo = 0
                self.display.set_combo(self.combo)
            self.active_gem_left += 1
        while self.active_gem_right < len(self.gems) and self.gems[self.active_gem_right][0] < time + 0.1:
            self.active_gem_right += 1
        
        while self.hold_active_gem_left < len(self.holds) and self.holds[self.hold_active_gem_left][0] < time - 0.1:
            # case 8: hold start pass
            if not self.hold_map[self.hold_active_gem_left] and not self.hold_map_lane[self.hold_active_gem_left]:
                print("pass hold no. ", self.hold_active_gem_left)
                self.audio_ctrl.set_mute(True)
                self.display.hold_pass(self.hold_active_gem_left)
                self.multiplier = max(1, self.multiplier - 0.03)
                self.combo = 0
                self.display.set_combo(self.combo)
            self.hold_active_gem_left += 1
        
        while self.hold_active_gem_right < len(self.holds) and self.holds[self.hold_active_gem_right][1] < time + self.holds[self.hold_active_gem_right][1] - self.holds[self.hold_active_gem_right][0] + 0.1:
            self.hold_active_gem_right += 1


if __name__ == "__main__":
    run(MainWidget())
