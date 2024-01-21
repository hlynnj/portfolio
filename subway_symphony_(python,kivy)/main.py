#
# Your final project goes here!
#

# This file just has a BaseWidget, nothing else.
# You may find ScreenManager helpful in your project.
# Check out the lecture7.py code for an example of that.

# (also, you don't have to use this code - feel free to delete this file and make a new main.py)

import sys, os
sys.path.insert(0, os.path.abspath('..'))

from imslib.core import run
from imslib.screen import ScreenManager

# import screens
from screens.intro_screen import IntroScreen
from screens.menu_screen import MenuScreen
from screens.game_screens import *
from screens.end_screen import EndScreen
from screens.tutorial_screen import TutorialScreen
from screens.win_screen import WinScreen

# init screen manager
sm = ScreenManager()

# add screens to screen manager
intro_screen = IntroScreen(name='intro')
sm.add_screen(intro_screen)

menu_screen = MenuScreen(name='menu')
sm.add_screen(menu_screen)

tutorial_screen = TutorialScreen(name='tutorial')
sm.add_screen(tutorial_screen)

game_screen_1 = GameScreen1(name='trepak')
sm.add_screen(game_screen_1)

game_screen_2 = GameScreen2(name='waltz')
sm.add_screen(game_screen_2)

end_screen = EndScreen(name='end')
sm.add_screen(end_screen)

win_screen = WinScreen(name='win')
sm.add_screen(win_screen)

# run the screen manager
run(sm)
