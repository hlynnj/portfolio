from imslib.gfxutil import topleft_label, CEllipse, KFAnim, AnimGroup, CRectangle

from kivy.core.window import Window
from kivy.graphics import Color

from math import *

time_span = 4.0
far_to_near_ratio = 1/3
theta = pi/4
nowbar_y = 0.1
post_height_ratio = 3 / 7
dz = 15
anim_color = Color(1,1,1)

def get_effective_width_ratio():
    width = Window.height * 4/3
    return width / Window.width

def map_coords_3D_to_2D(x,y,z):
    # given (x,y,z) coordinates in birdseye view, maps the coordinate to the (x,y) point on the window 
    width, height = Window.height * 4/3, Window.height

    norm_y = 1 - y / height
    if norm_y < 0:
        norm_y = 0 # should not appear on the screen
    final_y = (1-norm_y**2) * height

    ratio = final_y * (far_to_near_ratio - 1) / height + 1
    x_centered = x - Window.width / 2
    new_x = x_centered * ratio * width / Window.width
    final_x = new_x + Window.width / 2

    effective_z = z * ratio
    return (final_x, final_y*cos(theta) + effective_z)

    # norm_y = (1 - y / Window.height)
    # if norm_y < 0:
    #     return (-Window.width, -Window.height) # should not appear on the screen
    # return (new_x, new_y + sqrt(norm_y) *z)

def get_new_mode_alpha(color):
    if color.a == 1:
        return 0.5
    else:
        return 1

# convert a time value to a y-pixel value (where time==0 is on the nowbar)
def time_to_ypos(time):
    # (t, ypos) = (0, height*nowbar_h) (time_span, height*(1+nowbarh))
    # ypos = time*(height/time_span) +(height*nowbar_h)
    return time*Window.height/time_span + Window.height*nowbar_y

# take in a ypos relative to nowbar and return its time
def ypos_to_time(y):
    y_nowbar = Window.height * nowbar_y
    m = Window.height / time_span
    time = (y - y_nowbar) / m
    return time


class CTRectangle(CRectangle):
    """
    Override CRectangle class to add centered top functionality.
    Use *cpos* and *csize* to set/get the ellipse based on a centered-top registration point
    instead of a bottom-left registration point.
    """

    def __init__(self, **kwargs):
        super(CTRectangle, self).__init__(**kwargs)
        if 'ctpos' in kwargs:
            self.ctpos = kwargs['ctpos']

        if 'ctsize' in kwargs:
            self.ctsize = kwargs['ctsize']

    def get_ctpos(self):
        """
        The centered top position of the ellipse as a tuple `(x, y)`.
        """

        return (self.cpos[0], self.cpos[1] + self.size[1]/2)

    def set_ctpos(self, p):
        """
        Sets centered top position of the ellipse.

        :param p: The new centered position as a tuple `(x, y)`.
        """

        self.cpos = (p[0], p[1] - self.size[1]/2)

    def get_ctsize(self):
        """
        The current size of the ellipse as a tuple `(width, height)`.
        """

        return self.size

    def set_ctsize(self, p):
        """
        Sets the size of the ellipse.

        :param p: The new size as a tuple `(width, height)`.
        """

        ctpos = self.get_ctpos()
        self.size = p
        self.set_ctpos(ctpos)

    ctpos = property(get_ctpos, set_ctpos)
    ctsize = property(get_ctsize, set_ctsize)


class CBEllipse(CEllipse):
    """
    Override Ellipse class to add centered bottom functionality.
    Use *cpos* and *csize* to set/get the ellipse based on a centered-bottom registration point
    instead of a bottom-left registration point.
    """

    def __init__(self, **kwargs):
        super(CBEllipse, self).__init__(**kwargs)
        if 'cbpos' in kwargs:
            self.cbpos = kwargs['cbpos']

        if 'cbsize' in kwargs:
            self.cbsize = kwargs['cbsize']

    def get_cbpos(self):
        """
        The centered top position of the ellipse as a tuple `(x, y)`.
        """

        return (self.cpos[0], self.cpos[1] - self.size[1]/2)

    def set_cbpos(self, p):
        """
        Sets centered bottom position of the ellipse.

        :param p: The new centered position as a tuple `(x, y)`.
        """

        self.cpos = (p[0], p[1] + self.size[1]/2)

    def get_cbsize(self):
        """
        The current size of the ellipse as a tuple `(width, height)`.
        """

        return self.size

    def set_cbsize(self, p):
        """
        Sets the size of the ellipse.

        :param p: The new size as a tuple `(width, height)`.
        """

        cbpos = self.get_cbpos()
        self.size = p
        self.set_cbpos(cbpos)

    cbpos = property(get_cbpos, set_cbpos)
    cbsize = property(get_cbsize, set_cbsize)
