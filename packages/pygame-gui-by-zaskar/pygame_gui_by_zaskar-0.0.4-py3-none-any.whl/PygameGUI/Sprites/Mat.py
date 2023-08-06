from .Sprite import Sprite
from .Sprite import NoCvMatSet
import pygame as pg

class Mat(Sprite):
    def __init__(self, par_surf, /,
                 cv_mat_stream=None,
                 **kwargs):

        if cv_mat_stream:
            self.cv_mat_stream = cv_mat_stream
        else:
            raise NoCvMatSet
        super().__init__(par_surf, **kwargs)
        self.is_mat_stream = False
        self.last_hover_pos = (0, 0)
        self.is_pressed = False

    def draw(self):
        mat = self.cv_mat_stream()
        if self.width != 0 and self.height != 0:
            self.rect = self.surface.blit(pg.transform.flip(
                pg.transform.scale(pg.transform.rotate(pg.surfarray.make_surface(mat), -90), (self.width, self.height)),
                1, 0), self.pos)
        else:
            self.rect = self.surface.blit(
                pg.transform.flip(pg.transform.rotate(pg.surfarray.make_surface(mat), -90), 1, 0),
                self.pos)

    def update(self):
        self.func(mouse_pos=self.last_hover_pos, btn_id=self.is_pressed)

    def pressed(self, *args, **kwargs):
        self.last_hover_pos = kwargs["mouse_pos"]
        self.is_pressed = kwargs["btn_id"]

    def dragged(self, *args, **kwargs):
        self.last_hover_pos = kwargs["mouse_pos"]
        self.is_pressed = kwargs["btn_id"]
        pass

    def hover(self, *args, **kwargs):
        self.last_hover_pos = kwargs["mouse_pos"]
        self.is_pressed = False
