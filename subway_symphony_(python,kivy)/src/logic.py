import re
from graphics.helper_funcs import *
from src.improv import ImprovManager
import random

######################
#   MappingManager   #
######################

# Assume mapping "gems" are in (time, lane, new_instr) such that each "gem" represents a lane to instrument mapping change for the specified lane with the specified instrument. Any time a mapping is changed, it defines that lane to be the LEAD instrument on which coins will be generated for.

# (1) Load mapping changes into array (copying over all information in the gems file)
# (2) get_map() returns list of mapping changes

# for parsing map text file: return (time, lane, instrument) from a single line of text
# time: float, lane: int, instrument: string name of new instrument
def map_from_line(line):
    print(re.split(';|\t', line.strip()))
    time, lane, instrument = re.split(';|\t', line.strip())
    return (float(time), int(lane), instrument)

class MapManager(object):

    def __init__(self, piece):
        super(MapManager, self).__init__()
        self.piece = piece
        map_file = f'./data/audio/{self.piece}/{self.piece}_map.txt'
        map_lines = open(map_file).readlines()
        self.mapping = [map_from_line(l) for l in map_lines]
    
    def get_map(self):
        return self.mapping

##################
#   GemManager   #
##################

# Assume gems are in (time, instrument, lane, is_jump)

# (1) Load gems into array (copying over all information in the gems file)
# (2) get_gems() returns the list of gems

# for parsing gem text file: return (time, is_jump, lane, instrument) from a single line of text
# time: float, instrument: string name, lane: int, is_jump: bool
def gem_from_line(line):
    time, is_jump, lane, instrument = re.split(';|\t', line.strip())
    return (float(time), bool(int(is_jump)), int(lane), instrument)

class GemManager(object):

    def __init__(self, piece):
        super(GemManager, self).__init__()
        self.piece = piece

        # gem_file = f'./data/gems/{self.piece}_gems.txt'
        # gem_lines = open(gem_file).readlines()
        # self.gems = [gem_from_line(l) for l in gem_lines]

        # for testing purposes
        # self.gems = [(3, 0, 1, 'violin'), (6, 0, 1, 'violin'), (9, 1, 1, 'violin'), (12, 1, 2, 'horn')]
        self.gems = [(3, 1, 1, 'violin'), (6, 1, 2, 'violin'), (9, 0, 0, 'violin')]

        # NOTE: jaden - i was thinking maybe we can keep graphics for obstacles/coins here instead of in game_screen
        # so that the Player can change the graphics for them when hit/pass occurs
        # mainly so that we can access the actual Coin/Obstacle objects and modify them in Player for on_hit(), etc.
        self.obstacles = []
        self.coins = []

    def get_gems(self):
        return self.gems
    

###########################
#   Gems to Map Checker   #
###########################
# Checks the following invariants of the gems and mapping arrays:
# (1) for a given time, the lead instrument and the gem instrument should match
# (2) for a given time, the lead lane and the gem lane should match

# NOTE: potentially, this could be moved so that the GemManager class automatically assumes a certain lead instrument based on mapping, but probably for the purposes of authoring gems, it is easier to explicitly state what gems are for which instruments (so we don't accidentally write for the wrong instrument)
def check_gems_to_map(gems, mapping):
    # TODO
    pass


##############
#   Player   #
##############

# Assets: - Gems
#         - Current Lead Lane
#         - Current Player Lane
#         - Previous Player Lane
#         - Current Lane to Instrument Mapping
#         - Gem Pointer into next expected action

# Functions:
# (1) Change Player Lane, based on user input [1] if new lane is not lead, mute both prev and new lanes [2] if new lane is lead, unmute both prev and new lanes.
# (2) Change Lane to Instrument Mapping [1] if mapping change involves current player lane, start lane unmuted [2] otherwise mute lane with new mapping
# (3) on_action, check if user has taken action at the right time and in the right lane and corresponds with expected action (jump or tap) then update mute/unmute and score
# (4) on_update, progress gem pointer according to time (pass if elapsed time > 0.1 + expected time)

# IMPORTANT NOTE: implementation assumes mapping change for a lane will occur some moments after the last note in the previous mapping and some moments before the first note in the new mapping. That is, mapping change SHOULD NOT coincide too closely with a gem, as much as possible.

# NOTE:
# (1) level offering / instrument choice

class Player(object):

    def __init__(self, map_manager, gem_manager=None, audio_ctrl=None, improv_ctrl=None, game_display=None, thresh=0.1, init_lane=1):
        super(Player, self).__init__()
    
        # two data structures (arrays) we need to keep track of
        self.gems = gem_manager.get_gems() # (time, is_jump, lane, instrument)
        # print(self.gems)

        self.mapping = map_manager.get_map() # (time, lane, instrument)

        # manage lanes (for mute/unmute purposes)
        self.prev_lane = init_lane # int (0, 1, 2)
        self.curr_lane = init_lane # int (0, 1, 2)
        self.lead_lane = self.mapping[0][1] # int (0, 1, 2)
        self.prev_instr = self.mapping[0][2]
        self.lead_instr = self.mapping[0][2]

        # audio manager
        self.audio_ctrl = audio_ctrl
        self.audio_ctrl.on_lead_change(self.lead_instr)
        if self.curr_lane != self.lead_lane:
            self.audio_ctrl.set_gain(self.lead_instr, 0)
        else:
            self.audio_ctrl.set_gain(self.lead_instr, 1)

        # sliding window of active gems based on current time
        self.gem_left_idx = 0
        self.gem_right_idx = 0

        # indicator if gem has been hit
        self.gem_hit = {idx: False for idx in range (len(self.gems))}

        # pointer to next lead lane / instrument change
        self.map_idx = 1

        # score-related things
        self.thresh = thresh # time threshold for note hits
        self.hit_score = 200 # score per coin collected
        self.miss_score = 10 # score decreased per coin missed
        self.collide_score = 100 # score decreased per train side collision
        self.score = 0 # cumulative score
        self.streak = 0
        self.improv_score = 5000

        # game display
        self.game_display = game_display
        self.game_display.set_collide_callback(self.collide_train_side)
    
        # # improv manager
        # self.improv_ctrl = improv_ctrl
        # self.improv_ctrl.set_end_callback(self.change_mode)
        # self.improv_ctrl.set_text_change_callback(self.game_display.set_improv_text)
        # self.improv_time = 37.4 # for testing purposes
        # self.improv_done = False
        self.mode = 'reg' # 'reg' for regular, 'improv' for improv

        # improv token that controls improv or not
        # improv token params are defined in game_display
        self.improv_time = self.game_display.improv_token.get_time()
        self.improv_lane = self.game_display.improv_token.get_lane()
        self.improv_checked = False
        self.audio_ctrl.set_improv_end_callback(self.change_mode)


    ###################################
    #   Game Mode Related Functions   #
    ###################################

    def reset(self, game_display):
        # called by the app when the game is over

        self.prev_lane = 1 # int (0, 1, 2)
        self.curr_lane = 1 # int (0, 1, 2)
        self.lead_lane = self.mapping[0][1] # int (0, 1, 2)
        self.prev_instr = self.mapping[0][2]
        self.lead_instr = self.mapping[0][2]

        self.audio_ctrl.reset()
        self.audio_ctrl.on_lead_change(self.lead_instr)
        if self.curr_lane != self.lead_lane:
            self.audio_ctrl.set_gain(self.lead_instr, 0)
        else:
            self.audio_ctrl.set_gain(self.lead_instr, 1)
        
        self.gem_left_idx = 0
        self.gem_right_idx = 0

        self.gem_hit = {idx: False for idx in range (len(self.gems))}

        self.map_idx = 1

        self.game_display = game_display
        self.game_display.set_collide_callback(self.collide_train_side)

        self.score = 0
        self.streak = 0
        self.mode = 'reg'

        self.improv_time = self.game_display.improv_token.get_time()
        self.improv_lane = self.game_display.improv_token.get_lane()
        self.improv_checked = False
        self.audio_ctrl.set_improv_end_callback(self.change_mode)

    def change_mode(self):
        # switches between improv and reg
        # when does it switch to improv? based on self.improv_time
        # when does it switch back to reg? when improv is over, as determined in the ImprovManager class (when the appropriate number of measures have gone by)
        print('prev mode ', self.mode)
        if self.mode == 'reg':
            self.mode = 'improv'
            self.audio_ctrl.start_improv()
            self.score += self.improv_score
        elif self.mode == 'improv':
            self.mode = 'reg'
        self.game_display.switch_mode()
        
        print('changed mode to ', self.mode)
    

    ################################
    #   Responding to User Input   #
    ################################

    # dispatcher based on user input
    def on_player_action(self, keycode):

        if keycode == "left" or keycode == "right":
            self.change_player_lane(direction=keycode)
        elif keycode == "spacebar":
            if self.mode == 'reg':
                self.on_tap()
            else:
                self.game_display.improv_icon.on_hit()
                self.audio_ctrl.on_tap()
        elif keycode == "up":
            if self.mode == 'reg':
                self.on_jump()
            else:
                pass
    
    def change_player_lane(self, direction):

        assert (direction == "right" or direction == "left")

        # case: cannot move left from left-most lane, cannot move right from right-most lane
        if (self.curr_lane == 0 and direction == "left") or (self.curr_lane == 2 and direction == "right"):
            return
        
        # change player lane
        self.prev_lane = self.curr_lane
        incr = 1 if direction == "right" else -1
        self.curr_lane = self.curr_lane + incr

        # manage improv controller lane
        # self.improv_ctrl.change_player_lane(self.curr_lane)
    
    # get all gems (coins) on screen in the slop window
    def get_slop_coins(self):
        slop_coins = {}
        for idx, coin in enumerate(self.game_display.coins): # coin is Coin object
            if abs(ypos_to_time(coin.get_y_pos())) < self.thresh:
                slop_coins[coin.get_lane()] = (idx, coin)
        return slop_coins

    def on_tap(self):
        # # NOTE: for loop to account for multiple gems within the threshold time, but probably removable if we don't have taps happening that fast
        # for i in range(self.gem_left_idx, self.gem_right_idx):
        #     # tap in the correct lane
        #     if self.curr_lane == self.lead_lane and not self.gems[i][1]:
        #         print("hit tap no. ", i)
        #         self.score += self.hit_score
        #         self.gem_hit[i] = True
        #         self.audio_ctrl.set_gain(self.lead_instr, 1)
        #     # TODO: display tap graphics

        # NOTE: jaden - using slop_gem method to see if button press is a hit or not
        slop_coins = self.get_slop_coins()
        if self.curr_lane in slop_coins: # we hit the correct gem
            # print('hit!')
            idx, coin = slop_coins[self.curr_lane] # gem is Coin object
            coin.on_hit()
            self.game_display.instrument_icon.on_hit()
            self.score += self.hit_score
            # self.gem_hit[idx] = True
            self.audio_ctrl.set_gain(self.lead_instr, 1)
            self.streak += 1
        else: # missed gem
            # print('miss!')
            self.audio_ctrl.set_gain(self.lead_instr, 0)
            self.audio_ctrl.play_miss()
            for idx, coin in slop_coins.values():
                coin.on_pass()
                self.game_display.instrument_icon.on_pass()
                self.score -= self.miss_score

    
    def on_jump(self):

        for i in range(self.gem_left_idx, self.gem_right_idx):
            # jump in the correct lane
            if self.curr_lane == self.lead_lane and self.gems[i][1]:
                # print("hit jump no. ", i)
                self.streak += 1
                self.score += self.hit_score
                self.gem_hit[i] = True
                self.audio_ctrl.set_gain(self.lead_instr, 1)
            # TODO: display jump graphics
    

    ############################################
    #   Update Functions (Constantly Called)   #
    ############################################

    def collision_check(self):
        pass

    
    def get_pass_coins(self):
        for idx, coin in enumerate(self.game_display.coins):
            if ypos_to_time(coin.get_y_pos()) < -0.1 and not coin.hit and not coin.passed:
                # print('pass!')
                self.streak = 0
                coin.on_pass()
                self.game_display.instrument_icon.on_pass()
                self.score -= self.miss_score
                self.audio_ctrl.set_gain(self.lead_instr, 0)
                self.audio_ctrl.play_miss()

    def collide_train_side(self):
        self.score -= self.collide_score
        self.audio_ctrl.play_side_train()

    def on_update(self, time):

        if self.mode == 'reg':

            # # change mode if needed
            # if not self.improv_done and time > self.improv_time:
            #     self.change_mode()
            #     self.improv_done = True
            
            # change to improv mode if player collects the improv token
            if not self.improv_checked and time > self.improv_time:
                if self.curr_lane == self.improv_lane:
                    self.change_mode()
                    self.game_display.improv_token.on_collect()
                else:
                    self.game_display.improv_token.on_pass()
                self.improv_checked = True

            # change mapping if needed
            if self.map_idx < len(self.mapping) and time > self.mapping[self.map_idx][0]:

                self.prev_instr = self.mapping[self.map_idx-1][2]
                self.curr_instr = self.mapping[self.map_idx][2]
                self.lead_lane = self.mapping[self.map_idx][1]
                self.prev_instr = self.lead_instr
                self.lead_instr = self.mapping[self.map_idx][2]
                self.map_idx += 1

                self.audio_ctrl.on_lead_change(self.lead_instr)

                self.audio_ctrl.set_gain(self.prev_instr, 1)

                # update mute/unmute on mapping change
                if self.curr_lane == self.lead_lane:
                    self.audio_ctrl.set_gain(self.lead_instr, 1)
                else:
                    self.audio_ctrl.set_gain(self.lead_instr, 0)
                
                self.game_display.instrument_icon.change_instrument(self.lead_instr)
            
            # # change gem sliding window as needed
            # # and calculate misses as necessary
            # while self.gem_left_idx < len(self.gems) and self.gems[self.gem_left_idx][0] < time - self.thresh:
            #     if not self.gem_hit[self.gem_left_idx]:
            #         print("pass gem no. ", self.gem_left_idx)
            #         self.audio_ctrl.set_gain(self.lead_instr, 0)
            #         # TODO: pass graphics
            #     self.gem_left_idx += 1
            
            # while self.gem_right_idx < len(self.gems) and self.gems[self.gem_right_idx][0] < time + self.thresh:
            #     self.gem_right_idx += 1

            self.get_pass_coins()

            self.game_display.set_score(self.score)
            self.game_display.set_streak(self.streak)


####################
#   ScoreManager   #
####################

class ScoreManager(object):

    def __init__(self):
        super(ScoreManager, self).__init__()
        self.scores = []
    
    def get_scores(self):
        return self.scores
    
    def add_score(self, score):
        self.scores = sorted(self.scores + [score], reverse=True)
        if len(self.scores) > 10:
            self.scores = self.score[:10]