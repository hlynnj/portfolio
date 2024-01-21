import sys, os
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('./graphics'))

from imslib.gfxutil import topleft_label, CEllipse, AnimGroup, CLabelRect
from imslib.screen import Screen
from imslib.clock import Clock, SimpleTempoMap, Scheduler, quantize_tick_up

from kivy.core.window import Window
from kivy.uix.button import Button
from kivy import metrics

from src.logic import GemManager, MapManager, Player
from src.audio import AudioController
# from src.improv import ImprovManager
from src.song_data import SongData

from graphics.game_display import GameDisplay

from kivy.clock import Clock as kivyClock


font_sz = metrics.dp(20)
button_sz = metrics.dp(100)



# TREPAK
class GameScreen1(Screen):
    def __init__(self, **kwargs):
        super(GameScreen1, self).__init__(**kwargs)

        # set up logic things
        self.gem_manager = GemManager('Nutcracker')
        self.map_manager = MapManager('Nutcracker')
        self.audio_ctrl = AudioController("Trepak", './data/audio/Nutcracker/Nutcracker')

        # set up song data
        self.map_filepath = './data/audio/Nutcracker/Nutcracker_map.txt'
        self.gem_filepath = './data/audio/Nutcracker/Nutcracker_gems.txt'
        self.song_data = SongData(self.map_filepath, self.gem_filepath)

        # set up graphics
        self.game_display = GameDisplay(self.song_data, self.game_over, 'Trepak')
        self.canvas.add(self.game_display)

        # set up logic player w/ graphics
        self.player = Player(game_display=self.game_display, gem_manager=self.gem_manager, map_manager=self.
        map_manager, audio_ctrl=self.audio_ctrl)

        # text for debugging
        self.info = topleft_label()
        self.add_widget(self.info)

        self.tempo_map = SimpleTempoMap(60)
        self.clock = Clock()
        self.sched = Scheduler(self.clock, self.tempo_map)

    def on_enter(self):

        # essentially re-init the game system

        # set up graphics
        # set up logic things
        self.gem_manager = GemManager('Nutcracker')
        self.map_manager = MapManager('Nutcracker')
        self.audio_ctrl = AudioController("Trepak", './data/audio/Nutcracker/Nutcracker')

        # set up song data
        self.map_filepath = './data/audio/Nutcracker/Nutcracker_map.txt'
        self.gem_filepath = './data/audio/Nutcracker/Nutcracker_gems.txt'
        self.song_data = SongData(self.map_filepath, self.gem_filepath)

        # set up graphics
        self.game_display = GameDisplay(self.song_data, self.game_over, 'Trepak')
        self.canvas.add(self.game_display)

        # set up logic player w/ graphics
        self.player = Player(game_display=self.game_display, gem_manager=self.gem_manager, map_manager=self.
        map_manager, audio_ctrl=self.audio_ctrl)

        # text for debugging
        self.info = topleft_label()
        self.add_widget(self.info)

        self.tempo_map = SimpleTempoMap(60)
        self.clock = Clock()
        self.sched = Scheduler(self.clock, self.tempo_map)

        self.audio_ctrl.toggle()

    def on_key_down(self, keycode, modifiers):
        # manage graphics
        self.game_display.on_key_down(keycode, modifiers)

        # play / pause toggle
        # if keycode[1] == 'p':
        #     self.audio_ctrl.toggle()
        
        # get player action
        if keycode[1] == 'left':
            self.player.on_player_action(keycode[1])
        if keycode[1] == 'right':
            self.player.on_player_action(keycode[1])
        if keycode[1] == 'up':
            self.player.on_player_action(keycode[1])
        if keycode[1] == 'spacebar':
            self.player.on_player_action(keycode[1])
        
        # # force mode change for now
        # if keycode[1] == 'm':
        #     self.player.change_mode()
        
        # # NOTE: force screen change during development
        # # TODO: change to game over condition
        # if keycode[1] == 'q':
        #     self.switch_to('end')
        #     self.player.reset()

    def game_over(self):

        print("GAME OVER")
        self.audio_ctrl.on_game_over()

        # reset graphics screen
        self.canvas.remove(self.game_display)
        self.game_display = GameDisplay(self.song_data, self.game_over, 'Trepak')
        self.canvas.add(self.game_display)

        now = self.sched.get_tick()
        game_over_delay_in_sec = 0
        self.sched.post_at_tick(self.game_over_callback, now+480*game_over_delay_in_sec) # go to game over screen in x seconds
    
    def game_over_callback(self, tick):

        self.switch_to('end', {'score': self.player.score})
        # self.player.reset(self.game_display)
    
    def on_update(self):
        # manage audio
        self.audio_ctrl.on_update()
        now = self.audio_ctrl.get_time()

        if now > 67.73:
            print("game win!")
            print("Final Score: " + str(self.player.score))
            self.switch_to('win', {'score': self.player.score})

        # manage logic
        self.player.on_update(now)

        # manage graphics
        self.game_display.on_update(now)

        if self.audio_ctrl.waiting:
            self.info.text = f"starting in {self.audio_ctrl.start_counter + 1}"
        else:
            self.info.text = f'fps:{kivyClock.get_fps():.0f}\n'
        
        self.sched.on_update()

        # print(len(self.game_display.children))
        
    def on_resize(self, win_size):
        self.game_display.on_resize(win_size)





# WALTZ OF THE FLOWERS
# NOTE: Currently loads in the same thing as Trepak
class GameScreen2(Screen):
    def __init__(self, **kwargs):
        super(GameScreen2, self).__init__(**kwargs)

        # set up logic things
        self.gem_manager = GemManager('Waltz')
        self.map_manager = MapManager('Waltz')
        self.audio_ctrl = AudioController("Waltz", './data/audio/Waltz/Waltz')

        # set up song data
        self.map_filepath = './data/audio/Waltz/Waltz_map.txt'
        self.gem_filepath = './data/audio/Waltz/Waltz_gems.txt'
        self.song_data = SongData(self.map_filepath, self.gem_filepath)

        # set up graphics
        self.game_display = GameDisplay(self.song_data, self.game_over, 'Waltz')
        self.canvas.add(self.game_display)

        # set up logic player w/ graphics
        self.player = Player(game_display=self.game_display, gem_manager=self.gem_manager, map_manager=self.
        map_manager, audio_ctrl=self.audio_ctrl)

        # text for debugging
        self.info = topleft_label()
        self.add_widget(self.info)

        self.tempo_map = SimpleTempoMap(60)
        self.clock = Clock()
        self.sched = Scheduler(self.clock, self.tempo_map)

    def on_enter(self):

        # essentially re-init the game system

        # set up graphics
        # set up logic things
        self.gem_manager = GemManager('Waltz')
        self.map_manager = MapManager('Waltz')
        self.audio_ctrl = AudioController("Waltz", './data/audio/Waltz/Waltz')

        # set up song data
        self.map_filepath = './data/audio/Waltz/Waltz_map.txt'
        self.gem_filepath = './data/audio/Waltz/Waltz_gems.txt'
        self.song_data = SongData(self.map_filepath, self.gem_filepath)

        # set up graphics
        self.game_display = GameDisplay(self.song_data, self.game_over, 'Waltz')
        self.canvas.add(self.game_display)

        # set up logic player w/ graphics
        self.player = Player(game_display=self.game_display, gem_manager=self.gem_manager, map_manager=self.
        map_manager, audio_ctrl=self.audio_ctrl)

        # text for debugging
        self.info = topleft_label()
        self.add_widget(self.info)

        self.tempo_map = SimpleTempoMap(60)
        self.clock = Clock()
        self.sched = Scheduler(self.clock, self.tempo_map)

        self.audio_ctrl.toggle()

    def on_key_down(self, keycode, modifiers):
        # manage graphics
        self.game_display.on_key_down(keycode, modifiers)

        # play / pause toggle
        # if keycode[1] == 'p':
        #     self.audio_ctrl.toggle()
        
        # get player action
        if keycode[1] == 'left':
            self.player.on_player_action(keycode[1])
        if keycode[1] == 'right':
            self.player.on_player_action(keycode[1])
        if keycode[1] == 'up':
            self.player.on_player_action(keycode[1])
        if keycode[1] == 'spacebar':
            self.player.on_player_action(keycode[1])
        
        # # force mode change for now
        # if keycode[1] == 'm':
        #     self.player.change_mode()
        
        # # NOTE: force screen change during development
        # # TODO: change to game over condition
        # if keycode[1] == 'q':
        #     self.switch_to('end')
        #     self.player.reset()

    def game_over(self):

        print("GAME OVER")
        self.audio_ctrl.toggle()
        self.audio_ctrl.on_game_over()

        # reset graphics screen
        self.canvas.remove(self.game_display)
        self.game_display = GameDisplay(self.song_data, self.game_over, 'Waltz')
        self.canvas.add(self.game_display)

        now = self.sched.get_tick()
        game_over_delay_in_sec = 0
        self.sched.post_at_tick(self.game_over_callback, now+480*game_over_delay_in_sec) # go to game over screen in x seconds
    
    def game_over_callback(self, tick):

        self.switch_to('end', {'score': self.player.score})
        # self.player.reset(self.game_display)
    
    def on_update(self):
        # manage audio
        self.audio_ctrl.on_update()
        now = self.audio_ctrl.get_time()
        # print(now)
        if now > 206.35:
            print("game win!")
            print("Final Score: " + str(self.player.score))
            self.switch_to('win', {'score': self.player.score})

        # manage logic
        self.player.on_update(now)

        # manage graphics
        self.game_display.on_update(now)

        if self.audio_ctrl.waiting:
            self.info.text = f"starting in {self.audio_ctrl.start_counter + 1}"
        else:
            self.info.text = f'fps:{kivyClock.get_fps():.0f}\n'
        
        self.sched.on_update()

        # print(len(self.game_display.children))
        
    def on_resize(self, win_size):
        self.game_display.on_resize(win_size)