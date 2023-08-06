import pygame as pg

class NoCvMatSet(Exception):
    """Raised when no cv mat set for object of class Mat"""
    pass


class NoDrawFuncReloaded(Exception):
    """Raised when sprite draw func is not reloaded in child class"""
    pass


class Sprite:
    def __init__(self, par_surf, /,
                 name="Sprite",
                 x=0,
                 y=0,
                 width=0,
                 height=0,
                 func=lambda *args, **kwargs: args,
                 color=(100, 100, 100),
                 transparent_for_mouse=False,
                 **kwargs):
        self.func = func
        self.name = name
        self.par_surf = par_surf
        self.surface = self.par_surf.screen
        self.ps_width, self.ps_height = par_surf.width, par_surf.height
        self.x = int(x * self.ps_width)
        self.y = int(y * self.ps_height)
        self.pos = self.x, self.y
        self.width = int(width * self.ps_width)
        self.height = int(height * self.ps_height)
        self.color = color
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)
        self.transparent_for_mouse = transparent_for_mouse

    def pressed(self, *args, **kwargs):
        pass

    def dragged(self, *args, **kwargs):
        pass

    def release(self, *args, **kwargs):
        pass

    def hover(self, *args, **kwargs):
        pass

    def update(self):
        pass

    def convert_to_local(self, coords):
        return coords[0] - self.x, coords[1] - self.y

    def set_pos(self, pos):
        self.pos = pos[0]*self.ps_width, pos[1]*self.ps_height
        self.x = pos[0]*self.ps_width
        self.y = pos[1]*self.ps_height

    def draw(self):
        raise NoDrawFuncReloaded