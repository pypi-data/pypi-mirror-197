import pygame as pg

from .Sprite import Sprite


class Text(Sprite):
    def __init__(self, par_surf, /,
                 inp_text=lambda *args: "your text",
                 color=(255, 255, 255),
                 font='serif',
                 font_size=10, **kwargs):
        super().__init__(par_surf, color=color, **kwargs)
        self.inp_text = inp_text
        self.text = pg.font.SysFont(font, int(font_size * self.ps_height / 500))
        self.txt_render = self.text.render(str(self.inp_text()), True, self.color)

    def pressed(self, *args, **kwargs):
        self.func(args, **kwargs)

    def update(self):
        self.txt_render = self.text.render(str(self.inp_text()), True, self.color)

    def draw(self):
        self.rect = self.surface.blit(self.txt_render, self.pos)
