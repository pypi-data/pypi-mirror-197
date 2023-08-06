from .Sprite import Sprite
import pygame as pg


class Button(Sprite):
    def __init__(self, par_surf, /, image="", radius=10, **kwargs):
        super().__init__(par_surf, **kwargs)
        self.radius = radius
        if image:

            if isinstance(image, str):
                self.have_image = 1
                self.image = pg.transform.scale(pg.image.load(image), (self.width, self.height))

            else:
                self.have_image = len(image)
                self.image_arr = []
                for img in image:
                    self.image_arr.append(pg.transform.scale(pg.image.load(img), (self.width, self.height)))
                self.image = self.image_arr[0]
                self.curr_img = 0
        else:
            self.have_image = 0

    def pressed(self, *args, **kwargs):
        self.func(*args, **kwargs)

    def draw(self):
        if self.have_image == 1:
            self.surface.blit(self.image, self.rect)
        elif self.have_image > 1:
            self.surface.blit(self.image_arr[self.curr_img], self.rect)
        else:
            pg.draw.rect(self.surface, self.color, self.rect, border_radius=self.radius)
