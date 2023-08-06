__all__ = ["Slider"]

from .Sprite import Sprite
import pygame as pg


def range_cut(mi, ma, val):
    return min(ma, max(mi, val))


def convert_range(new_min, new_max, old_min, old_max, old_value):
    old_range = (old_max - old_min)
    new_range = (new_max - new_min)
    return (((old_value - old_min) * new_range) / old_range) + new_min


class Slider(Sprite):
    def __init__(self, par_surf, /,
                 slider_color=(255, 255, 255),
                 min=0,
                 max=100,
                 val=None, **kwargs):
        super().__init__(par_surf, **kwargs)
        self.slider_color = slider_color
        self.min = min
        self.max = max
        self.slider_rad = self.height // 2
        self.slider_y = self.slider_rad

        if val:
            self.val = val
        else:
            self.val = self.min

        self.slider_x = convert_range(self.slider_rad, self.width - self.slider_rad, self.min, self.max, self.val)

    def set_val(self, val):
        self.slider_x = convert_range(self.slider_rad, self.width - self.slider_rad, self.min, self.max, val)

    def dragged(self, *args, **kwargs):
        pos = kwargs["mouse_pos"]
        self.slider_x = range_cut(self.slider_rad, self.width - self.slider_rad, pos[0])
        self.val = convert_range(self.min, self.max, self.slider_rad, self.width - self.slider_rad, self.slider_x)
        self.func(self.val)

    def update(self):
        pg.draw.rect(self.surface, self.color, (0, 0, self.width, self.height), border_radius=self.height // 2)
        pg.draw.circle(self.surface, (255, 255, 255), (self.slider_x, self.slider_y), self.slider_rad)

    def draw(self):
        self.slider_x = convert_range(self.slider_rad, self.width - self.slider_rad, self.min, self.max, self.val)
        pg.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height),
                     border_radius=self.height // 2)
        pg.draw.circle(self.surface, (255, 255, 255), (self.x + self.slider_x, self.y + self.slider_y), self.slider_rad)

